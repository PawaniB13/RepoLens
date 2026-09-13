package com.repolens.backend.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/analysis")
public class AnalysisTriggerController {

    @PostMapping("/trigger")
    public ResponseEntity<String> triggerAnalysis(
            @RequestParam String repository,
            @RequestParam(defaultValue = "main") String branch
    ) {
        String message = String.format(
                "Analysis triggered for repository %s on branch %s",
                repository,
                branch
        );

        System.out.println(message);

        return ResponseEntity.ok(message);
    }
}