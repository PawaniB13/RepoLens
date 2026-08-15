package com.repolens.backend;

import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.service.RepositoryAnalysisService;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RepositoryAnalysisServiceTest {

    @Test
    void shouldAnalyzeRepository() {
        RepositoryAnalysisService service = new RepositoryAnalysisService();

        RepositoryAnalysis result = service.analyzeRepository(1L);

        assertNotNull(result);
        assertEquals(1L, result.getRepositoryId());
        assertEquals("RepoLens", result.getRepositoryName());
        assertEquals(10, result.getTotalFiles());
        assertEquals(5, result.getJavaFiles());
        assertEquals(3, result.getJavascriptFiles());
    }
}