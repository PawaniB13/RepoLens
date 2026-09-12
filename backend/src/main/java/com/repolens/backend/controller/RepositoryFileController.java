package com.repolens.backend.controller;

import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.service.RepositoryFileService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryFileController {

    private final RepositoryFileService repositoryFileService;

    public RepositoryFileController(
            RepositoryFileService repositoryFileService) {
        this.repositoryFileService = repositoryFileService;
    }

    @GetMapping("/{repositoryId}/files")
    public ResponseEntity<List<RepositoryFile>> getFiles(
            @PathVariable Long repositoryId) {

        if (repositoryId == null || repositoryId <= 0) {
            throw new IllegalArgumentException(
                    "Repository ID must be positive"
            );
        }

        return ResponseEntity.ok(
                repositoryFileService.getFiles(repositoryId)
        );
    }
}
