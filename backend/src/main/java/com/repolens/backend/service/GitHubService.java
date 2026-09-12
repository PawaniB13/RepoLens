package com.repolens.backend.service;

import com.repolens.backend.model.RepositoryFile;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Service
public class GitHubService {

    private final RestClient restClient;

public GitHubService() {
    this.restClient = RestClient.create("https://api.github.com");
}

    public List<RepositoryFile> getRepositoryFiles(String owner, String repo) {

        String apiPath = "/repos/" + owner + "/" + repo + "/git/trees/HEAD?recursive=1";

        Map<String, Object> response = restClient.get()
                .uri(apiPath)
                .retrieve()
                .body(new ParameterizedTypeReference<>() {});

        List<RepositoryFile> files = new ArrayList<>();

        if (response == null || response.get("tree") == null) {
            return files;
        }

        List<Map<String, Object>> tree =
                (List<Map<String, Object>>) response.get("tree");

        for (Map<String, Object> item : tree) {

            String type = String.valueOf(item.get("type"));

            if (!"blob".equals(type)) {
                continue;
            }

            String path = String.valueOf(item.get("path"));
            String language = detectLanguage(path);

            files.add(new RepositoryFile(
                    extractFileName(path),
                    language,
                    path
            ));
        }

        return files;
    }

    private String extractFileName(String path) {
        int lastSlash = path.lastIndexOf('/');
        return lastSlash >= 0 ? path.substring(lastSlash + 1) : path;
    }

    private String detectLanguage(String path) {

        String lowerPath = path.toLowerCase();

        if (lowerPath.endsWith(".java")) return "Java";
        if (lowerPath.endsWith(".js")) return "JavaScript";
        if (lowerPath.endsWith(".ts")) return "TypeScript";
        if (lowerPath.endsWith(".py")) return "Python";
        if (lowerPath.endsWith(".html")) return "HTML";
        if (lowerPath.endsWith(".css")) return "CSS";
        if (lowerPath.endsWith(".json")) return "JSON";
        if (lowerPath.endsWith(".md")) return "Markdown";

        return "Other";
    }
}