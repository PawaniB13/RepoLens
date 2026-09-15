package com.repolens.backend.controller;

import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.service.RepositoryAnalysisService;
import com.repolens.backend.service.RepositoryService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/analysis")
public class AnalysisTriggerController {

    private final RepositoryService repositoryService;
    private final RepositoryAnalysisService repositoryAnalysisService;

    public AnalysisTriggerController(
            RepositoryService repositoryService,
            RepositoryAnalysisService repositoryAnalysisService
    ) {
        this.repositoryService = repositoryService;
        this.repositoryAnalysisService = repositoryAnalysisService;
    }

    @PostMapping("/trigger")
    public ResponseEntity<?> triggerAnalysis(
            @RequestParam String repository,
            @RequestParam(defaultValue = "main") String branch
    ) {
        List<Repository> repositories =
                repositoryService.searchRepositories(repository);

        if (repositories.isEmpty()) {
            return ResponseEntity.notFound().build();
        }

        Repository selectedRepository = repositories.get(0);

        if (selectedRepository.getId() == null) {
            return ResponseEntity.internalServerError()
                    .body("Repository ID is missing");
        }

        RepositoryAnalysis analysis =
                repositoryAnalysisService.analyzeRepository(
                        selectedRepository.getId()
                );

        return ResponseEntity.ok(analysis);
    }
}
