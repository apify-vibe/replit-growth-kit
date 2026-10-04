router.post('/api/schedules', createSchedule);
router.post('/api/shifts/:id/swap', requestSwap);
router.get('/api/labour-cost', labourCost);
router.post('/api/locations', createLocation); // one restaurant = one location
