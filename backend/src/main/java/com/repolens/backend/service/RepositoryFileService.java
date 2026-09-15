package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.repository.RepositoryFileRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class RepositoryFileService {

    private final RepositoryService repositoryService;
    private final RepositoryFileRepository repositoryFileRepository;
    private final RestClient restClient;

    public RepositoryFileService(
            RepositoryService repositoryService,
            RepositoryFileRepository repositoryFileRepository
    ) {
        this.repositoryService = repositoryService;
        this.repositoryFileRepository = repositoryFileRepository;
        this.restClient = RestClient.builder()
                .baseUrl("https://api.github.com")
                .build();
    }

    public List<RepositoryFile> getFiles(Long repositoryId) {
        List<RepositoryFile> storedFiles =
                repositoryFileRepository.findByRepositoryId(repositoryId);

        if (storedFiles != null && !storedFiles.isEmpty()) {
            return storedFiles;
        }

        Repository repository =
                repositoryService.getRepository(repositoryId);

        return loadFilesFromGitHub(repository);
    }

    public List<RepositoryFile> refreshFiles(Long repositoryId) {
        Repository repository =
                repositoryService.getRepository(repositoryId);

        List<RepositoryFile> latestFiles =
                loadFilesFromGitHub(repository);

        repository.getFiles().clear();

        for (RepositoryFile file : latestFiles) {
            repository.addFile(file);
        }

        repositoryService.saveRepository(repository);

        return repositoryFileRepository
                .findByRepositoryId(repositoryId);
    }

    public List<RepositoryFile> refreshFilesByRepositoryUrl(
            String repositoryUrl
    ) {
        Repository repository = repositoryService
                .getRepositories()
                .stream()
                .filter(item -> repositoryUrl.equals(item.getUrl()))
                .findFirst()
                .orElseThrow(() ->
                        new IllegalArgumentException(
                                "Repository not found for URL: "
                                        + repositoryUrl
                        )
                );

        return refreshFiles(repository.getId());
    }

    public String getFileContent(
            Long repositoryId,
            String filePath
    ) {
        Repository repository =
                repositoryService.getRepository(repositoryId);

        String[] parts = repository.getUrl()
                .replace("https://github.com/", "")
                .split("/");

        if (parts.length < 2) {
            throw new IllegalArgumentException(
                    "Invalid GitHub repository URL"
            );
        }

        String owner = parts[0];
        String repo = parts[1];

        Map<String, Object> response = restClient.get()
                .uri("/repos/{owner}/{repo}/contents/{path}",
                        owner,
                        repo,
                        filePath)
                .retrieve()
                .body(Map.class);

        if (response == null || response.get("content") == null) {
            return "";
        }

        return response.get("content").toString();
    }

    private List<RepositoryFile> loadFilesFromGitHub(
            Repository repository
    ) {
        String[] parts = repository.getUrl()
                .replace("https://github.com/", "")
                .split("/");

        if (parts.length < 2) {
            throw new IllegalArgumentException(
                    "Invalid GitHub repository URL"
            );
        }

        String owner = parts[0];
        String repo = parts[1];

        Map<String, Object> repositoryData =
                getGitHubRepository(owner, repo);

        String defaultBranch =
                getStringValue(repositoryData, "default_branch");

        if (defaultBranch == null) {
            defaultBranch = "main";
        }

        Map<String, Object> branchData = restClient.get()
                .uri("/repos/{owner}/{repo}/git/refs/heads/{branch}",
                        owner,
                        repo,
                        defaultBranch)
                .retrieve()
                .body(Map.class);

        if (branchData == null) {
            return List.of();
        }

        Map<String, Object> object =
                castMap(castMap(branchData.get("object")));

        String treeSha =
                getStringValue(object, "sha");

        if (treeSha == null) {
            return List.of();
        }

        Map<String, Object> treeData = restClient.get()
                .uri("/repos/{owner}/{repo}/git/trees/{sha}?recursive=1",
                        owner,
                        repo,
                        treeSha)
                .retrieve()
                .body(Map.class);

        if (treeData == null) {
            return List.of();
        }

        Object treeValue = treeData.get("tree");

        if (!(treeValue instanceof List<?> tree)) {
            return List.of();
        }

        List<RepositoryFile> files = new ArrayList<>();

        for (Object item : tree) {
            Map<String, Object> fileData =
                    castMap(item);

            String type =
                    getStringValue(fileData, "type");

            String path =
                    getStringValue(fileData, "path");

            if (!"blob".equals(type) || path == null) {
                continue;
            }

            String fileName = getFileName(path);
            String fileType = getFileType(fileName);

            files.add(
                    new RepositoryFile(
                            fileName,
                            fileType,
                            path
                    )
            );
        }

        return files;
    }

    private Map<String, Object> getGitHubRepository(
            String owner,
            String repo
    ) {
        Map<String, Object> response = restClient.get()
                .uri("/repos/{owner}/{repo}", owner, repo)
                .retrieve()
                .body(Map.class);

        return response == null ? Map.of() : response;
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> castMap(Object value) {
        if (!(value instanceof Map<?, ?>)) {
            return Map.of();
        }

        return (Map<String, Object>) value;
    }

    private String getStringValue(
            Map<String, Object> data,
            String key
    ) {
        Object value = data.get(key);

        return value == null ? null : value.toString();
    }

    private String getFileName(String path) {
        int lastSlash = path.lastIndexOf("/");

        if (lastSlash < 0) {
            return path;
        }

        return path.substring(lastSlash + 1);
    }

    private String getFileType(String fileName) {
        int lastDot = fileName.lastIndexOf(".");

        if (lastDot < 0) {
            return "unknown";
        }

        return fileName.substring(lastDot + 1)
                .toLowerCase();
    }
}