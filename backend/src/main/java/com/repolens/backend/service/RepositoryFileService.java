package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.repository.RepositoryFileRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.Map;

@Service
public class RepositoryFileService {

    private final RepositoryService repositoryService;
    private final RepositoryFileRepository repositoryFileRepository;
    private final RestClient restClient;

    @Autowired
    public RepositoryFileService(
            RepositoryService repositoryService,
            RepositoryFileRepository repositoryFileRepository
    ) {
        this.repositoryService = repositoryService;
        this.repositoryFileRepository = repositoryFileRepository;

        this.restClient = RestClient.builder()
                .baseUrl("https://api.github.com")
                .defaultHeader(
                        "Accept",
                        "application/vnd.github+json"
                )
                .defaultHeader(
                        "X-GitHub-Api-Version",
                        "2022-11-28"
                )
                .build();
    }

    public List<RepositoryFile> getFiles(Long repositoryId) {
        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException(
                    "Repository ID must be positive"
            );
        }

        Repository repository =
                repositoryService.getRepository(repositoryId);

        /*
         * Return files already stored in the database.
         * This prevents normal GET requests and tests from
         * unnecessarily calling GitHub.
         */
        List<RepositoryFile> storedFiles =
                repositoryFileRepository.findByRepositoryId(repositoryId);

        if (storedFiles != null && !storedFiles.isEmpty()) {
            return storedFiles;
        }

        /*
         * If no files are stored yet, load them from GitHub.
         */
        Map<?, ?> repositoryResponse =
                getGitHubRepository(repository);

        String[] repositoryParts =
                parseGitHubRepository(repository.getUrl());

        String owner = repositoryParts[0];
        String repo = repositoryParts[1];

        String defaultBranch = getStringValue(
                repositoryResponse,
                "default_branch",
                "main"
        );

        Map<?, ?> treeResponse = restClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path(
                                "/repos/{owner}/{repo}/git/trees/{branch}"
                        )
                        .queryParam("recursive", "1")
                        .build(
                                owner,
                                repo,
                                defaultBranch
                        ))
                .retrieve()
                .body(Map.class);

        if (treeResponse == null) {
            throw new IllegalArgumentException(
                    "GitHub repository files could not be loaded"
            );
        }

        Object treeObject = treeResponse.get("tree");

        if (!(treeObject instanceof List<?>)) {
            throw new IllegalArgumentException(
                    "GitHub repository tree is invalid"
            );
        }

        List<RepositoryFile> files = new ArrayList<>();

        for (Object item : (List<?>) treeObject) {
            if (!(item instanceof Map<?, ?>)) {
                continue;
            }

            Map<?, ?> itemMap = (Map<?, ?>) item;

            if (!"blob".equals(
                    String.valueOf(itemMap.get("type"))
            )) {
                continue;
            }

            String path = String.valueOf(
                    itemMap.get("path")
            );

            RepositoryFile file = new RepositoryFile(
                    getFileName(path),
                    getFileType(path),
                    path
            );

            file.setRepository(repository);
            files.add(file);
        }

        return files;
    }

    public List<RepositoryFile> refreshFiles(Long repositoryId) {
        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException(
                    "Repository ID must be positive"
            );
        }

        Repository repository =
                repositoryService.getRepository(repositoryId);

        repository.getFiles().clear();

        List<RepositoryFile> latestFiles =
                loadFilesFromGitHub(repository);

        for (RepositoryFile file : latestFiles) {
            repository.addFile(file);
        }

        repositoryService.saveRepository(repository);

        return repositoryFileRepository
                .findByRepositoryId(repositoryId);
    }

    public Map<?, ?> getGitHubRepositoryMetadata(Long repositoryId) {
        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException(
                    "Repository ID must be positive"
            );
        }

        Repository repository =
                repositoryService.getRepository(repositoryId);

        return getGitHubRepository(repository);
    }

    public String getFileContent(
            Long repositoryId,
            String path
    ) {
        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException(
                    "Repository ID must be positive"
            );
        }

        if (path == null || path.isBlank()) {
            throw new IllegalArgumentException(
                    "File path is required"
            );
        }

        Repository repository =
                repositoryService.getRepository(repositoryId);

        String[] repositoryParts =
                parseGitHubRepository(repository.getUrl());

        String owner = repositoryParts[0];
        String repo = repositoryParts[1];

        Map<?, ?> response = restClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path(
                                "/repos/{owner}/{repo}/contents/{path}"
                        )
                        .build(
                                owner,
                                repo,
                                path
                        ))
                .retrieve()
                .body(Map.class);

        if (response == null) {
            throw new IllegalArgumentException(
                    "GitHub file content was not found"
            );
        }

        Object contentObject = response.get("content");

        if (!(contentObject instanceof String)) {
            throw new IllegalArgumentException(
                    "GitHub did not return file content"
            );
        }

        String cleanContent = ((String) contentObject)
                .replace("\n", "")
                .replace("\r", "")
                .trim();

        byte[] decodedBytes =
                Base64.getMimeDecoder().decode(cleanContent);

        return new String(
                decodedBytes,
                StandardCharsets.UTF_8
        );
    }

    private List<RepositoryFile> loadFilesFromGitHub(
            Repository repository
    ) {
        Map<?, ?> repositoryResponse =
                getGitHubRepository(repository);

        String[] repositoryParts =
                parseGitHubRepository(repository.getUrl());

        String owner = repositoryParts[0];
        String repo = repositoryParts[1];

        String defaultBranch = getStringValue(
                repositoryResponse,
                "default_branch",
                "main"
        );

        Map<?, ?> treeResponse = restClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path(
                                "/repos/{owner}/{repo}/git/trees/{branch}"
                        )
                        .queryParam("recursive", "1")
                        .build(
                                owner,
                                repo,
                                defaultBranch
                        ))
                .retrieve()
                .body(Map.class);

        if (treeResponse == null) {
            throw new IllegalArgumentException(
                    "GitHub repository files could not be loaded"
            );
        }

        Object treeObject = treeResponse.get("tree");

        if (!(treeObject instanceof List<?>)) {
            throw new IllegalArgumentException(
                    "GitHub repository tree is invalid"
            );
        }

        List<RepositoryFile> files = new ArrayList<>();

        for (Object item : (List<?>) treeObject) {
            if (!(item instanceof Map<?, ?>)) {
                continue;
            }

            Map<?, ?> itemMap = (Map<?, ?>) item;

            if (!"blob".equals(
                    String.valueOf(itemMap.get("type"))
            )) {
                continue;
            }

            String path = String.valueOf(
                    itemMap.get("path")
            );

            RepositoryFile file = new RepositoryFile(
                    getFileName(path),
                    getFileType(path),
                    path
            );

            file.setRepository(repository);
            files.add(file);
        }

        return files;
    }

    private Map<?, ?> getGitHubRepository(
            Repository repository
    ) {
        String[] repositoryParts =
                parseGitHubRepository(repository.getUrl());

        return restClient.get()
                .uri(
                        "/repos/{owner}/{repo}",
                        repositoryParts[0],
                        repositoryParts[1]
                )
                .retrieve()
                .body(Map.class);
    }

    private String getStringValue(
            Map<?, ?> map,
            String key,
            String defaultValue
    ) {
        Object value = map.get(key);

        if (value == null
                || String.valueOf(value).isBlank()) {
            return defaultValue;
        }

        return String.valueOf(value);
    }

    private String[] parseGitHubRepository(String url) {
        if (url == null || url.isBlank()) {
            throw new IllegalArgumentException(
                    "Repository URL is required"
            );
        }

        String cleanUrl = url
                .trim()
                .replace("https://github.com/", "")
                .replace("http://github.com/", "")
                .replace("github.com/", "")
                .replaceAll("/+$", "");

        String[] parts = cleanUrl.split("/");

        if (parts.length < 2) {
            throw new IllegalArgumentException(
                    "Invalid GitHub repository URL: " + url
            );
        }

        return new String[]{
                parts[0],
                parts[1].replaceAll("\\.git$", "")
        };
    }

    private String getFileName(String path) {
        int lastSlash = path.lastIndexOf('/');

        if (lastSlash >= 0) {
            return path.substring(lastSlash + 1);
        }

        return path;
    }

    private String getFileType(String path) {
        int lastDot = path.lastIndexOf('.');

        if (lastDot < 0 || lastDot == path.length() - 1) {
            return "Unknown";
        }

        String extension = path.substring(lastDot + 1);

        return extension.substring(0, 1).toUpperCase()
                + extension.substring(1);
    }
}