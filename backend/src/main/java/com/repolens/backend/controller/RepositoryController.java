package com.repolens.backend.controller;

import com.repolens.backend.dto.GitHubImportRequest;
import com.repolens.backend.model.Repository;
import com.repolens.backend.service.GitHubService;
import com.repolens.backend.service.RepositoryService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryController {

    private final RepositoryService repositoryService;
    private final GitHubService gitHubService;

    public RepositoryController(RepositoryService repositoryService) {
        this.repositoryService = repositoryService;
        this.gitHubService = null;
    }

    @Autowired
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
    public ResponseEntity<Repository> getRepository(
            @PathVariable Long id) {

        return repositoryService.getRepositories()
                .stream()
                .filter(repository ->
                        repository.getId().equals(id))
                .findFirst()
                .map(ResponseEntity::ok)
                .orElseGet(() ->
                        ResponseEntity.notFound().build());
    }

    @GetMapping("/search")
    public List<Repository> searchRepositories(
            @RequestParam String query) {

        return repositoryService.searchRepositories(query);
    }

    @PostMapping("/import")
    public ResponseEntity<Repository> importRepository(
            @RequestBody GitHubImportRequest request) {

        if (gitHubService == null) {
            return ResponseEntity.internalServerError().build();
        }

        Repository repository = gitHubService.importRepository(
                request.getOwner(),
                request.getRepo()
        );

        return ResponseEntity.ok(repository);
    }
}
