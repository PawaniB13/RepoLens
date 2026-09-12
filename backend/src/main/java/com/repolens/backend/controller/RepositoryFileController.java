package com.repolens.backend.controller;

import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.service.GitHubService;
import com.repolens.backend.service.RepositoryFileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryFileController {

    private final GitHubService gitHubService;
    private final RepositoryFileService repositoryFileService;

    // Existing tests ke liye old constructor
    public RepositoryFileController(RepositoryFileService repositoryFileService) {
        this.repositoryFileService = repositoryFileService;
        this.gitHubService = null;
    }

    // Spring Boot ke liye new constructor
    @Autowired
    public RepositoryFileController(
            GitHubService gitHubService,
            RepositoryFileService repositoryFileService) {

        this.gitHubService = gitHubService;
        this.repositoryFileService = repositoryFileService;
    }

    @GetMapping("/{repositoryId}/files")
    public ResponseEntity<List<RepositoryFile>> getFiles(
            @PathVariable Long repositoryId) {

        // Temporary mapping: repository ID 1 -> GitHub repository
        if (repositoryId != null && repositoryId == 1 && gitHubService != null) {

            List<RepositoryFile> files =
                    gitHubService.getRepositoryFiles(
                            "spring-projects",
                            "spring-boot"
                    );

            return ResponseEntity.ok(files);
        }

        // Old test/mock behavior
        if (repositoryFileService != null) {
            return ResponseEntity.ok(
                    repositoryFileService.getFiles(repositoryId)
            );
        }

        return ResponseEntity.notFound().build();
    }
}