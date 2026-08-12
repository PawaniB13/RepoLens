package com.repolens.backend.service;

import org.springframework.stereotype.Service;

@Service
public class HealthService {

    public String getHealthStatus() {
        return "RepoLens backend is running";
    }
}