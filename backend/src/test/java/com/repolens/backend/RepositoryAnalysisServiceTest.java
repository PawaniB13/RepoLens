package com.repolens.backend;

import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.repository.RepositoryFileRepository;
import com.repolens.backend.service.RepositoryAnalysisService;
import com.repolens.backend.service.RepositoryFileService;
import com.repolens.backend.service.RepositoryService;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.*;

class RepositoryAnalysisServiceTest {

    @Test
    void shouldAnalyzeRepositoryFiles() {
        RepositoryService repositoryService = mock(RepositoryService.class);
        RepositoryFileService repositoryFileService = mock(RepositoryFileService.class);
        RepositoryFileRepository repositoryFileRepository = mock(RepositoryFileRepository.class);

        Repository repository = new Repository(
                "spring-projects/spring-petclinic",
                "https://github.com/spring-projects/spring-petclinic"
        );


       when(repositoryService.getRepository(4L)).thenReturn(repository);

        List<RepositoryFile> files = List.of(
                new RepositoryFile("Application.java", "java", "src/Application.java"),
                new RepositoryFile("App.java", "java", "src/App.java"),
                new RepositoryFile("script.js", "javascript", "src/script.js")
        );

        when(repositoryFileService.getFiles(4L)).thenReturn(files);

        RepositoryAnalysisService analysisService =
                new RepositoryAnalysisService(repositoryService, repositoryFileService);

        var analysis = analysisService.analyzeRepository(4L);

        assertEquals(4L, analysis.getRepositoryId());
        assertEquals("spring-projects/spring-petclinic", analysis.getRepositoryName());
        assertEquals(3, analysis.getTotalFiles());
        assertEquals(2, analysis.getJavaFiles());
        assertEquals(1, analysis.getJavascriptFiles());

        verify(repositoryService).getRepository(4L);
        verify(repositoryFileService).getFiles(4L);
    }
}