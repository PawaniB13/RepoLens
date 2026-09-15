package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class GitHubService {

    private final RepositoryService repositoryService;
    private final RestClient restClient;

    public GitHubService(RepositoryService repositoryService) {
        this.repositoryService = repositoryService;

        this.restClient = RestClient.builder()
                .baseUrl("https://api.github.com")
                .defaultHeader(
                        "Accept",
                        "application/vnd.github+json"
                )
                .build();
    }

    public Repository importRepository(String owner, String repo) {
        validateRepositoryInput(owner, repo);

        Map<String, Object> response =
                fetchRepository(owner, repo);

        String fullName =
                (String) response.get("full_name");

        String htmlUrl =
                (String) response.get("html_url");

        if (fullName == null || htmlUrl == null) {
            throw new IllegalArgumentException(
                    "Invalid response from GitHub"
            );
        }

        return repositoryService.importRepository(
                fullName,
                htmlUrl
        );
    }

    public Repository refreshRepository(String owner, String repo) {
        validateRepositoryInput(owner, repo);

        Map<String, Object> response =
                fetchRepository(owner, repo);

        String fullName =
                (String) response.get("full_name");

        String htmlUrl =
                (String) response.get("html_url");

        if (fullName == null || htmlUrl == null) {
            throw new IllegalArgumentException(
                    "Invalid response from GitHub"
            );
        }

        return repositoryService.importRepository(
                fullName,
                htmlUrl
        );
    }

    private Map<String, Object> fetchRepository(
            String owner,
            String repo
    ) {
        Map<String, Object> response = restClient.get()
                .uri(
                        "/repos/{owner}/{repo}",
                        owner,
                        repo
                )
                .retrieve()
                .body(
                        new ParameterizedTypeReference<
                                Map<String, Object>
                        >() {}
                );

        if (response == null) {
            throw new IllegalArgumentException(
                    "GitHub repository not found"
            );
        }

        return response;
    }

    private void validateRepositoryInput(
            String owner,
            String repo
    ) {
        if (owner == null || owner.isBlank()
                || repo == null || repo.isBlank()) {
            throw new IllegalArgumentException(
                    "Owner and repository name are required"
            );
        }
    }
}