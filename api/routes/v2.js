const express = require('express');
const router = express.Router();
const { hikerApiRequest } = require('../hikerApiUtil'); 

  // V2 endpoints
  router.get('/user/by/id', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/user/by/id', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/by/username', async (req, res) => {
    try {
      const { username } = req.query;
      const data = await hikerApiRequest('GET', '/user/by/username', { username });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/userstream/by/username', async (req, res) => {
    try {
      const { username } = req.query;
      const data = await hikerApiRequest('GET', '/userstream/by/username', { username });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/stories', async (req, res) => {
    try {
      const { user_id } = req.query;
      const data = await hikerApiRequest('GET', '/user/stories', { user_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/stories/by/username', async (req, res) => {
    try {
      const { username } = req.query;
      const data = await hikerApiRequest('GET', '/user/stories/by/username', { username });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/medias', async (req, res) => {
    try {
      const { user_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/user/medias', { user_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });

  
  router.get('/user/clips', async (req, res) => {
    try {
      const { user_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/user/clips', { user_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/videos', async (req, res) => {
    try {
      const { user_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/user/videos', { user_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/following', async (req, res) => {
    try {
      const { user_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/user/following', { user_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/followers', async (req, res) => {
    try {
      const { user_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/user/followers', { user_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/tag/medias', async (req, res) => {
    try {
      const { user_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/user/tag/medias', { user_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/highlights', async (req, res) => {
    try {
      const { user_id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/user/highlights', { user_id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/highlights/by/username', async (req, res) => {
    try {
      const { username, amount } = req.query;
      const data = await hikerApiRequest('GET', '/user/highlights/by/username', { username, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/by/id', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/media/by/id', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/by/code', async (req, res) => {
    try {
      const { code } = req.query;
      const data = await hikerApiRequest('GET', '/media/by/code', { code });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/by/url', async (req, res) => {
    try {
      const { url } = req.query;
      const data = await hikerApiRequest('GET', '/media/by/url', { url });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/comments', async (req, res) => {
    try {
      const { id, can_support_threading, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/media/comments', { id, can_support_threading, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/likers', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/media/likers', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/template', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/media/template', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/comment/offensive', async (req, res) => {
    try {
      const { media_id, comment } = req.query;
      const data = await hikerApiRequest('GET', '/media/comment/offensive', { media_id, comment });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/story/by/id', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/story/by/id', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/story/by/url', async (req, res) => {
    try {
      const { url } = req.query;
      const data = await hikerApiRequest('GET', '/story/by/url', { url });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/track/by/canonical/id', async (req, res) => {
    try {
      const { canonical_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/track/by/canonical/id', { canonical_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/track/by/id', async (req, res) => {
    try {
      const { track_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/track/by/id', { track_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/track/stream/by/id', async (req, res) => {
    try {
      const { track_id, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/track/stream/by/id', { track_id, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/hashtag/by/name', async (req, res) => {
    try {
      const { name } = req.query;
      const data = await hikerApiRequest('GET', '/hashtag/by/name', { name });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/hashtag/medias/top', async (req, res) => {
    try {
      const { name, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/hashtag/medias/top', { name, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/hashtag/medias/recent', async (req, res) => {
    try {
      const { name, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/hashtag/medias/recent', { name, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/hashtag/medias/clips', async (req, res) => {
    try {
      const { name, page_id } = req.query;
      const data = await hikerApiRequest('GET', '/hashtag/medias/clips', { name, page_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/highlight/by/id', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/highlight/by/id', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  module.exports = router;