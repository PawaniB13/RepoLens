package com.repolens.backend.controller;

import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.service.RepositoryAnalysisService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryAnalysisController {

    private final RepositoryAnalysisService repositoryAnalysisService;

    public RepositoryAnalysisController(RepositoryAnalysisService repositoryAnalysisService) {
        this.repositoryAnalysisService = repositoryAnalysisService;
    }

    @GetMapping("/{repositoryId}/analysis")
    public RepositoryAnalysis analyzeRepository(@PathVariable Long repositoryId) {
        return repositoryAnalysisService.analyzeRepository(repositoryId);
    }
}