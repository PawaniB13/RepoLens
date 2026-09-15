package com.repolens.backend;

import com.repolens.backend.controller.RepositoryStatisticsController;
import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryFile;
import com.repolens.backend.model.RepositoryStatistics;
import com.repolens.backend.repository.RepositoryFileRepository;
import com.repolens.backend.service.RepositoryFileService;
import com.repolens.backend.service.RepositoryService;
import com.repolens.backend.service.RepositoryStatisticsService;
import org.junit.jupiter.api.Test;
import org.springframework.http.ResponseEntity;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class RepositoryStatisticsControllerTest {

    @Test
    void shouldGetRepositoryStatistics() {
        RepositoryService repositoryService = mock(RepositoryService.class);
        RepositoryFileRepository fileRepository = mock(RepositoryFileRepository.class);

        RepositoryFileService fileService =
                new RepositoryFileService(repositoryService, fileRepository);

        Repository repository = new Repository(
                "RepoLens",
                "https://github.com/example/RepoLens"
        );

        when(repositoryService.getRepository(1L)).thenReturn(repository);

        List<RepositoryFile> files = List.of(
                new RepositoryFile("One.java", "Java", "src/One.java"),
                new RepositoryFile("Two.java", "Java", "src/Two.java"),
                new RepositoryFile("Three.java", "Java", "src/Three.java")
        );

        when(fileRepository.findByRepositoryId(1L)).thenReturn(files);

        RepositoryStatisticsService service =
                new RepositoryStatisticsService(fileService);

        RepositoryStatisticsController controller =
                new RepositoryStatisticsController(service);

        ResponseEntity<RepositoryStatistics> response =
                controller.getStatistics(1L);

        assertEquals(200, response.getStatusCode().value());
        assertNotNull(response.getBody());
        assertEquals(1L, response.getBody().getRepositoryId());
        assertEquals("RepoLens", response.getBody().getRepositoryName());
        assertEquals(3, response.getBody().getTotalFiles());
        assertEquals(3, response.getBody().getJavaFiles());
        assertEquals(0, response.getBody().getJavascriptFiles());
        assertEquals(0, response.getBody().getOtherFiles());
    }

    @Test
    void shouldRejectInvalidRepositoryId() {
        RepositoryService repositoryService = mock(RepositoryService.class);
        RepositoryFileRepository fileRepository = mock(RepositoryFileRepository.class);

        RepositoryFileService fileService =
                new RepositoryFileService(repositoryService, fileRepository);

        when(repositoryService.getRepository(0L))
                .thenThrow(new IllegalArgumentException("Repository not found: 0"));

        RepositoryStatisticsService service =
                new RepositoryStatisticsService(fileService);

        RepositoryStatisticsController controller =
                new RepositoryStatisticsController(service);

        assertThrows(
                IllegalArgumentException.class,
                () -> controller.getStatistics(0L)
        );
    }
}