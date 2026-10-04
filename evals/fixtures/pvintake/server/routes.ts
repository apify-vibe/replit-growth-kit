router.post('/api/e2b/ingest', ingestE2B);
router.post('/api/cases/:id/validate', validateAgainstEmaRules);
