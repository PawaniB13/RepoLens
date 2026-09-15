package com.repolens.backend.controller;

import com.repolens.backend.dto.GitHubImportRequest;
import com.repolens.backend.model.Repository;
import com.repolens.backend.service.GitHubService;
import com.repolens.backend.service.RepositoryService;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryController {

    private final RepositoryService repositoryService;
    private final GitHubService gitHubService;

    public RepositoryController(
            RepositoryService repositoryService,
            GitHubService gitHubService
    ) {
        this.repositoryService = repositoryService;
        this.gitHubService = gitHubService;
    }

    @GetMapping
    public List<Repository> getRepositories() {
        return repositoryService.getRepositories();
    }

    @GetMapping("/{id}")
    public Repository getRepositoryById(@PathVariable Long id) {
        return repositoryService.getRepositories()
                .stream()
                .filter(repository -> repository.getId().equals(id))
                .findFirst()
                .orElseThrow(() ->
                        new RuntimeException("Repository not found: " + id)
                );
    }

    @GetMapping("/search")
    public List<Repository> searchRepositories(
            @RequestParam(required = false) String query
    ) {
        return repositoryService.searchRepositories(query);
    }

    @PostMapping("/import")
    public Repository importRepository(
            @RequestBody GitHubImportRequest request
    ) {
        String[] parts = request.getRepo().split("/", 2);

        if (parts.length != 2) {
            throw new IllegalArgumentException(
                    "Repository must use owner/name format"
            );
        }

        return gitHubService.importRepository(parts[0], parts[1]);
    }
    @PostMapping("/refresh")
public Repository refreshRepository(
        @RequestBody GitHubImportRequest request
) {
    String[] parts = request.getRepo().split("/", 2);

    if (parts.length != 2) {
        throw new IllegalArgumentException(
                "Repository must use owner/name format"
        );
    }

    return gitHubService.refreshRepository(
            parts[0],
            parts[1]
    );
}

    @DeleteMapping("/{id}")
    public void deleteRepository(@PathVariable Long id) {
        repositoryService.deleteRepository(id);
    }
}