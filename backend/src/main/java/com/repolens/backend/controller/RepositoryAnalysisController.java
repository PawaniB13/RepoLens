package com.repolens.backend.controller;

import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.service.RepositoryAnalysisService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryAnalysisController {

    private final RepositoryAnalysisService analysisService;

    public RepositoryAnalysisController(
            RepositoryAnalysisService analysisService) {
        this.analysisService = analysisService;
    }

    @GetMapping("/{id}/analysis")
    public RepositoryAnalysis analyzeRepository(
            @PathVariable Long id) {

        return analysisService.analyzeRepository(id);
    }
}