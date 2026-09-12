package com.repolens.backend.service;

import com.repolens.backend.model.RepositoryFile;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.util.UriUtils;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import java.util.Map;

@Service
public class GitHubService {

    private final RestClient restClient;

    public GitHubService() {
        this.restClient = RestClient.builder()
                .baseUrl("https://api.github.com")
                .defaultHeader("Accept", "application/vnd.github+json")
                .defaultHeader("X-GitHub-Api-Version", "2022-11-28")
                .build();
    }

    public List<RepositoryFile> getRepositoryFiles(
            String owner,
            String repo) {

        if (owner == null || owner.isBlank()) {
            throw new IllegalArgumentException("GitHub owner is required");
        }

        if (repo == null || repo.isBlank()) {
            throw new IllegalArgumentException("GitHub repository name is required");
        }

        String apiPath = "/repos/" + owner + "/" + repo
                + "/git/trees/HEAD?recursive=1";

        Map<String, Object> response = restClient.get()
                .uri(apiPath)
                .retrieve()
                .body(new ParameterizedTypeReference<Map<String, Object>>() {});

        List<RepositoryFile> files = new ArrayList<>();

        if (response == null || response.get("tree") == null) {
            return files;
        }

        Object treeObject = response.get("tree");

        if (!(treeObject instanceof List<?> treeList)) {
            return files;
        }

        for (Object treeItemObject : treeList) {

            if (!(treeItemObject instanceof Map<?, ?> treeItem)) {
                continue;
            }

            String type = String.valueOf(treeItem.get("type"));

            if (!"blob".equals(type)) {
                continue;
            }

            String path = String.valueOf(treeItem.get("path"));

            String fileName = extractFileName(path);
            String language = detectLanguage(path);

            files.add(
                    new RepositoryFile(
                            fileName,
                            language,
                            path
                    )
            );
        }

        return files;
    }

    public String getFileContent(
            String owner,
            String repo,
            String path) {

        if (owner == null || owner.isBlank()) {
            throw new IllegalArgumentException("GitHub owner is required");
        }

        if (repo == null || repo.isBlank()) {
            throw new IllegalArgumentException("GitHub repository name is required");
        }

        if (path == null || path.isBlank()) {
            throw new IllegalArgumentException("File path is required");
        }

        String encodedPath = UriUtils.encodePath(
                path,
                StandardCharsets.UTF_8
        );

        String apiPath = "/repos/" + owner + "/" + repo
                + "/contents/" + encodedPath;

        Map<String, Object> response = restClient.get()
                .uri(apiPath)
                .retrieve()
                .body(new ParameterizedTypeReference<Map<String, Object>>() {});

        if (response == null) {
            return "";
        }

        Object contentObject = response.get("content");

        if (contentObject == null) {
            return "";
        }

        String encodedContent = String.valueOf(contentObject)
                .replace("\n", "")
                .replace("\r", "")
                .trim();

        if (encodedContent.isBlank()) {
            return "";
        }

        byte[] decodedBytes = Base64.getDecoder()
                .decode(encodedContent);

        return new String(
                decodedBytes,
                StandardCharsets.UTF_8
        );
    }

    private String extractFileName(String path) {

        int lastSlashIndex = path.lastIndexOf('/');

        if (lastSlashIndex >= 0) {
            return path.substring(lastSlashIndex + 1);
        }

        return path;
    }

    private String detectLanguage(String path) {

        String lowerPath = path.toLowerCase();

        if (lowerPath.endsWith(".java")) {
            return "Java";
        }

        if (lowerPath.endsWith(".js")) {
            return "JavaScript";
        }

        if (lowerPath.endsWith(".jsx")) {
            return "JavaScript";
        }

        if (lowerPath.endsWith(".ts")) {
            return "TypeScript";
        }

        if (lowerPath.endsWith(".tsx")) {
            return "TypeScript";
        }

        if (lowerPath.endsWith(".py")) {
            return "Python";
        }

        if (lowerPath.endsWith(".html")) {
            return "HTML";
        }

        if (lowerPath.endsWith(".css")) {
            return "CSS";
        }

        if (lowerPath.endsWith(".scss")) {
            return "SCSS";
        }

        if (lowerPath.endsWith(".json")) {
            return "JSON";
        }

        if (lowerPath.endsWith(".xml")) {
            return "XML";
        }

        if (lowerPath.endsWith(".yml")
                || lowerPath.endsWith(".yaml")) {
            return "YAML";
        }

        if (lowerPath.endsWith(".md")) {
            return "Markdown";
        }

        if (lowerPath.endsWith(".adoc")) {
            return "AsciiDoc";
        }

        if (lowerPath.endsWith(".sql")) {
            return "SQL";
        }

        if (lowerPath.endsWith(".gradle")) {
            return "Gradle";
        }

        if (lowerPath.endsWith(".properties")) {
            return "Properties";
        }

        if (lowerPath.endsWith(".sh")) {
            return "Shell";
        }

        if (lowerPath.endsWith(".bat")) {
            return "Batch";
        }

        if (lowerPath.endsWith(".dockerfile")
                || lowerPath.equals("dockerfile")) {
            return "Dockerfile";
        }

        return "Other";
    }
}