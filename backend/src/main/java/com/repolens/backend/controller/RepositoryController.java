package com.repolens.backend.controller;

import com.repolens.backend.dto.GitHubImportRequest;
import com.repolens.backend.model.Repository;
import com.repolens.backend.service.GitHubService;
import com.repolens.backend.service.RepositoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryController {

    private final RepositoryService repositoryService;
    private final GitHubService gitHubService;

    public RepositoryController(
            RepositoryService repositoryService,
            GitHubService gitHubService) {
        this.repositoryService = repositoryService;
        this.gitHubService = gitHubService;
    }

    @GetMapping
    public List<Repository> getRepositories() {
        return repositoryService.getRepositories();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Repository> getRepository(@PathVariable Long id) {
        return repositoryService.getRepositories()
                .stream()
                .filter(repository -> repository.getId().equals(id))
                .findFirst()
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @GetMapping("/search")
    public List<Repository> searchRepositories(
            @RequestParam String query) {
        return repositoryService.searchRepositories(query);
    }

    @PostMapping("/import")
    public ResponseEntity<?> importRepository(
            @RequestBody GitHubImportRequest request) {

        if (request.getUrl() == null || request.getUrl().isBlank()) {
            return ResponseEntity.badRequest()
                    .body("GitHub URL is required");
        }

        if (!request.getUrl().startsWith("https://github.com/")) {
            return ResponseEntity.badRequest()
                    .body("Only GitHub URLs are supported");
        }

        try {
            Repository repository =
                    gitHubService.importFromGitHub(request.getUrl());

            return ResponseEntity.ok(repository);

        } catch (Exception exception) {
            return ResponseEntity.badRequest()
                    .body("Unable to import repository: "
                            + exception.getMessage());
        }
    }
}