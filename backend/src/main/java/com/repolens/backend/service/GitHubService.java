package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class GitHubService {

    private final RestClient restClient = RestClient.builder()
            .baseUrl("https://api.github.com")
            .defaultHeader(HttpHeaders.ACCEPT, MediaType.APPLICATION_JSON_VALUE)
            .build();

    private final RepositoryService repositoryService;

    public GitHubService(RepositoryService repositoryService) {
        this.repositoryService = repositoryService;
    }

    public Repository importFromGitHub(String url) {
        String cleanUrl = url.trim()
                .replace("https://github.com/", "")
                .replace(".git", "")
                .replaceAll("/$", "");

        String[] parts = cleanUrl.split("/");

        if (parts.length < 2) {
            throw new IllegalArgumentException("Invalid GitHub repository URL");
        }

        String owner = parts[0];
        String repoName = parts[1];

        Map<String, Object> githubRepository = restClient.get()
                .uri("/repos/{owner}/{repo}", owner, repoName)
                .retrieve()
                .body(Map.class);

        if (githubRepository == null) {
            throw new IllegalArgumentException("GitHub repository not found");
        }

        String fullName = (String) githubRepository.get("full_name");
        String htmlUrl = (String) githubRepository.get("html_url");

        return repositoryService.importRepository(fullName, htmlUrl);
    }
}