router.post('/api/monitors', createMonitor);
router.get('/api/monitors/:id/checks', listChecks);
router.post('/api/alerts/channels', addAlertChannel);
router.get('/status/:slug', renderStatusPage);
