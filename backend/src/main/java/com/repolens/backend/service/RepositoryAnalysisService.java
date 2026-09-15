package com.repolens.backend.service;

import com.repolens.backend.model.Repository;
import com.repolens.backend.model.RepositoryAnalysis;
import com.repolens.backend.model.RepositoryFile;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class RepositoryAnalysisService {

    private final RepositoryService repositoryService;
    private final RepositoryFileService repositoryFileService;
    private final FastApiClient fastApiClient;

    public RepositoryAnalysisService(
            RepositoryService repositoryService,
            RepositoryFileService repositoryFileService,
            FastApiClient fastApiClient
    ) {
        this.repositoryService = repositoryService;
        this.repositoryFileService = repositoryFileService;
        this.fastApiClient = fastApiClient;
    }

    public RepositoryAnalysis analyzeRepository(Long repositoryId) {
        Repository repository =
                repositoryService.getRepository(repositoryId);

        List<RepositoryFile> files =
                repositoryFileService.getFiles(repositoryId);

        int totalFiles = files.size();

        int javaFiles = (int) files.stream()
                .filter(file ->
                        file.getFileName() != null
                                && file.getFileName()
                                .toLowerCase()
                                .endsWith(".java")
                )
                .count();

        int javascriptFiles = (int) files.stream()
                .filter(file ->
                        file.getFileName() != null
                                && (
                                file.getFileName()
                                        .toLowerCase()
                                        .endsWith(".js")
                                        || file.getFileName()
                                        .toLowerCase()
                                        .endsWith(".jsx")
                        )
                )
                .count();

        RepositoryAnalysis analysis =
                new RepositoryAnalysis(
                        repositoryId,
                        repository.getName(),
                        totalFiles,
                        javaFiles,
                        javascriptFiles
                );

        analysis.setDefaultBranch("main");

        try {
            Map<String, Object> fastApiResult =
                    fastApiClient.analyzeRepository(
                            repositoryId,
                            repository.getName(),
                            repository.getUrl()
                    );

            applyFastApiResult(analysis, fastApiResult);
        } catch (Exception exception) {
            analysis.setLanguage("analysis-unavailable");
        }

        return analysis;
    }

    private void applyFastApiResult(
            RepositoryAnalysis analysis,
            Map<String, Object> result
    ) {
        Object language = result.get("language");
        Object stars = result.get("stars");
        Object forks = result.get("forks");
        Object openIssues = result.get("open_issues");
        Object defaultBranch = result.get("default_branch");

        if (language != null) {
            analysis.setLanguage(language.toString());
        }

        if (stars instanceof Number value) {
            analysis.setStars(value.intValue());
        }

        if (forks instanceof Number value) {
            analysis.setForks(value.intValue());
        }

        if (openIssues instanceof Number value) {
            analysis.setOpenIssues(value.intValue());
        }

        if (defaultBranch != null) {
            analysis.setDefaultBranch(defaultBranch.toString());
        }
    }
}