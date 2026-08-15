package com.repolens.backend.controller;

import com.repolens.backend.model.RepositoryStatistics;
import com.repolens.backend.service.RepositoryStatisticsService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/repositories")
public class RepositoryStatisticsController {

    private final RepositoryStatisticsService repositoryStatisticsService;

    public RepositoryStatisticsController(
            RepositoryStatisticsService repositoryStatisticsService) {
        this.repositoryStatisticsService = repositoryStatisticsService;
    }

    @GetMapping("/{repositoryId}/statistics")
    public ResponseEntity<RepositoryStatistics> getStatistics(
            @PathVariable Long repositoryId) {

        return ResponseEntity.ok(
                repositoryStatisticsService.getStatistics(repositoryId)
        );
    }
}