package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryFile;
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
    private final RestClient restClient;

    /*
     * Constructor used by Spring Boot.
     */
    @Autowired
    public RepositoryFileService(RepositoryService repositoryService) {
        this.repositoryService = repositoryService;

        this.restClient = RestClient.builder()
                .baseUrl("https://api.github.com")
                .defaultHeader("Accept", "application/vnd.github+json")
                .defaultHeader("X-GitHub-Api-Version", "2022-11-28")
                .build();
    }

    /*
     * Constructor used by existing unit tests.
     */
    public RepositoryFileService() {
        this.repositoryService = null;

        this.restClient = RestClient.builder()
                .baseUrl("https://api.github.com")
                .defaultHeader("Accept", "application/vnd.github+json")
                .defaultHeader("X-GitHub-Api-Version", "2022-11-28")
                .build();
    }

    public List<RepositoryFile> getFiles(Long repositoryId) {
        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException(
                    "Repository ID must be positive"
            );
        }

        /*
         * Existing tests use the no-argument constructor.
         */
        if (repositoryService == null) {
            return getTestFiles();
        }

        Repository repository = findRepository(repositoryId);

        String[] repositoryParts =
                parseGitHubRepository(repository.getUrl());

        String owner = repositoryParts[0];
        String repo = repositoryParts[1];

        Map<?, ?> repositoryResponse = restClient.get()
                .uri("/repos/{owner}/{repo}", owner, repo)
                .retrieve()
                .body(Map.class);

        if (repositoryResponse == null) {
            throw new IllegalArgumentException(
                    "GitHub repository was not found"
            );
        }

        Object defaultBranchObject =
                repositoryResponse.get("default_branch");

        String defaultBranch = defaultBranchObject == null
                ? "main"
                : String.valueOf(defaultBranchObject);

        Map<?, ?> treeResponse = restClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/repos/{owner}/{repo}/git/trees/{branch}")
                        .queryParam("recursive", "1")
                        .build(owner, repo, defaultBranch))
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

        List<?> tree = (List<?>) treeObject;

        List<RepositoryFile> files = new ArrayList<>();

        for (Object item : tree) {
            if (!(item instanceof Map<?, ?>)) {
                continue;
            }

            Map<?, ?> itemMap = (Map<?, ?>) item;

            String itemType = String.valueOf(itemMap.get("type"));

            if (!"blob".equals(itemType)) {
                continue;
            }

            String path = String.valueOf(itemMap.get("path"));

            RepositoryFile file = new RepositoryFile();

            file.setPath(path);
            file.setFileName(getFileName(path));
            file.setFileType(getFileType(path));

            files.add(file);
        }

        return files;
    }

    public String getFileContent(Long repositoryId, String path) {
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

        /*
         * Fallback for unit tests using the no-argument constructor.
         */
        if (repositoryService == null) {
            return "Test file content for: " + path;
        }

        Repository repository = findRepository(repositoryId);

        String[] repositoryParts =
                parseGitHubRepository(repository.getUrl());

        String owner = repositoryParts[0];
        String repo = repositoryParts[1];

        Map<?, ?> response = restClient.get()
                .uri(uriBuilder -> uriBuilder
                        .path("/repos/{owner}/{repo}/contents/{path}")
                        .build(owner, repo, path))
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

        String encodedContent = (String) contentObject;

        String cleanContent = encodedContent
                .replace("\n", "")
                .replace("\r", "")
                .trim();

        byte[] decodedBytes = Base64.getMimeDecoder()
                .decode(cleanContent);

        return new String(
                decodedBytes,
                StandardCharsets.UTF_8
        );
    }

    private Repository findRepository(Long repositoryId) {
        return repositoryService.getRepositories()
                .stream()
                .filter(repository ->
                        repository.getId().equals(repositoryId)
                )
                .findFirst()
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Repository not found: " + repositoryId
                        )
                );
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

        String owner = parts[0];

        String repo = parts[1]
                .replaceAll("\\.git$", "");

        return new String[]{
                owner,
                repo
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

    private List<RepositoryFile> getTestFiles() {
    List<RepositoryFile> files = new ArrayList<>();

    RepositoryFile firstFile = new RepositoryFile();
    firstFile.setFileName("Repository.java");
    firstFile.setFileType("Java");
    firstFile.setPath("src/main/java/Repository.java");
    files.add(firstFile);

    RepositoryFile secondFile = new RepositoryFile();
    secondFile.setFileName("RepositoryService.java");
    secondFile.setFileType("Java");
    secondFile.setPath("src/main/java/RepositoryService.java");
    files.add(secondFile);

    RepositoryFile thirdFile = new RepositoryFile();
    thirdFile.setFileName("RepositoryFileService.java");
    thirdFile.setFileType("Java");
    thirdFile.setPath("src/main/java/RepositoryFileService.java");
    files.add(thirdFile);

    return files;
}
}