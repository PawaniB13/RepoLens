package com.repolens.backend;

import com.repolens.backend.controller.RepositoryAnalysisController;
import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.service.RepositoryAnalysisService;
import com.repolens.backend.service.RepositoryFileService;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RepositoryAnalysisControllerTest {

    @Test
    void shouldAnalyzeRepository() {

        RepositoryFileService fileService = new RepositoryFileService();

        RepositoryAnalysisService service =
                new RepositoryAnalysisService(fileService);

        RepositoryAnalysisController controller =
                new RepositoryAnalysisController(service);

        RepositoryAnalysis result =
                controller.analyzeRepository(1L);

        assertNotNull(result);
        assertEquals(1L, result.getRepositoryId());
        assertEquals("RepoLens", result.getRepositoryName());
        assertEquals(3, result.getTotalFiles());
        assertEquals(3, result.getJavaFiles());
        assertEquals(0, result.getJavascriptFiles());
    }
}