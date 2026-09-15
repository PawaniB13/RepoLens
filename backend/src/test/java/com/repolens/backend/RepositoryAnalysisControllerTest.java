package com.repolens.backend;

import com.repolens.backend.controller.RepositoryAnalysisController;
import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.service.RepositoryAnalysisService;
import com.repolens.backend.service.RepositoryFileService;
import com.repolens.backend.service.RepositoryService;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class RepositoryAnalysisControllerTest {

    @Test
    void shouldAnalyzeRepository() {
        RepositoryService repositoryService = mock(RepositoryService.class);
        RepositoryFileService fileService = mock(RepositoryFileService.class);

        Repository repository = new Repository(
                "RepoLens",
                "https://github.com/example/RepoLens"
        );

        when(repositoryService.getRepository(1L)).thenReturn(repository);

        List<RepositoryFile> files = List.of(
                new RepositoryFile("One.java", "java", "src/One.java"),
                new RepositoryFile("Two.java", "java", "src/Two.java"),
                new RepositoryFile("Three.java", "java", "src/Three.java")
        );

        when(fileService.getFiles(1L)).thenReturn(files);

        RepositoryAnalysisService service =
                new RepositoryAnalysisService(repositoryService, fileService);

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