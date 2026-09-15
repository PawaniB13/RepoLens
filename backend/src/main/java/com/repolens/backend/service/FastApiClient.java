package com.repolens.backend.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

import java.util.Map;

@Service
public class FastApiClient {

    private final RestClient restClient;

    public FastApiClient(
            @Value("${fastapi.base-url:http://localhost:8000}")
            String fastApiBaseUrl
    ) {
        this.restClient = RestClient.builder()
                .baseUrl(fastApiBaseUrl)
                .build();
    }

    public Map<String, Object> analyzeRepository(
            Long repositoryId,
            String repositoryName,
            String repositoryUrl
    ) {
        Map<String, Object> request = Map.of(
                "repository_id", repositoryId,
                "repository_name", repositoryName,
                "repository_url", repositoryUrl
        );

        Map<String, Object> response = restClient.post()
                .uri("/api/v1/analyze")
                .body(request)
                .retrieve()
                .body(Map.class);

        return response == null ? Map.of() : response;
    }
}