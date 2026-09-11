package com.repolens.backend;

import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.service.RepositoryAnalysisService;
import com.repolens.backend.service.RepositoryFileService;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class RepositoryAnalysisServiceTest {

    @Test
    void shouldAnalyzeRepository() {
        RepositoryFileService fileService = new RepositoryFileService();
        RepositoryAnalysisService service =
                new RepositoryAnalysisService(fileService);

        RepositoryAnalysis analysis = service.analyzeRepository(1L);

        assertEquals(1L, analysis.getRepositoryId());
        assertEquals("RepoLens", analysis.getRepositoryName());
        assertEquals(3, analysis.getTotalFiles());
        assertEquals(3, analysis.getJavaFiles());
        assertEquals(0, analysis.getJavascriptFiles());
    }

    @Test
    void shouldRejectNullRepositoryId() {
        RepositoryFileService fileService = new RepositoryFileService();
        RepositoryAnalysisService service =
                new RepositoryAnalysisService(fileService);

        IllegalArgumentException exception = assertThrows(
                IllegalArgumentException.class,
                () -> service.analyzeRepository(null)
        );

        assertEquals("Repository ID must be positive", exception.getMessage());
    }

    @Test
    void shouldRejectNonPositiveRepositoryId() {
        RepositoryFileService fileService = new RepositoryFileService();
        RepositoryAnalysisService service =
                new RepositoryAnalysisService(fileService);

        IllegalArgumentException exception = assertThrows(
                IllegalArgumentException.class,
                () -> service.analyzeRepository(0L)
        );

        assertEquals("Repository ID must be positive", exception.getMessage());
    }
}