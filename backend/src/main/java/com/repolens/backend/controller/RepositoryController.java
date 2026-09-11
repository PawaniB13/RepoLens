package com.repolens.backend.controller;

import com.repolens.backend.model.Repository;
import com.repolens.backend.service.RepositoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryController {

    private final RepositoryService repositoryService;

    public RepositoryController(RepositoryService repositoryService) {
        this.repositoryService = repositoryService;
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

    @PostMapping
    public ResponseEntity<Repository> createRepository(
            @RequestBody Repository repository) {

        Repository savedRepository =
                repositoryService.saveRepository(repository);

        return ResponseEntity.ok(savedRepository);
    }
}