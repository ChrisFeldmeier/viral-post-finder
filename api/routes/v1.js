const express = require('express');
const router = express.Router();
const { hikerApiRequest } = require('../hikerApiUtil'); 

 // V1 endpoints
router.get('/user/search/following', async (req, res) => {
    // Parameters: user_id (string, required) - The ID of the user.
    //             query (string, required) - The search query.
    // Description: Searches users by following users.
    try {
      const { user_id, query } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/search/following', { user_id, query });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/following', async (req, res) => {
    // Parameters: user_id (string, required) - The ID of the user.
    //             amount (number, optional) - The number of users to fetch.
    // Description: Fetches the first page of following users.
    try {
      const { user_id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/following', { user_id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/following/chunk', async (req, res) => {
    // Parameters: user_id (string, required) - The ID of the user.
    //             max_id (string, optional) - The max ID for pagination.
    // Description: Fetches a chunk of following users with cursor.
    try {
      const { user_id, max_id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/following/chunk', { user_id, max_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/followers', async (req, res) => {
    // Parameters: user_id (string, required) - The ID of the user.
    //             amount (number, optional) - The number of users to fetch.
    // Description: Fetches the first page of followers.
    try {
      const { user_id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/followers', { user_id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/followers/chunk', async (req, res) => {
    // Parameters: user_id (string, required) - The ID of the user.
    //             max_id (string, optional) - The max ID for pagination.
    // Description: Fetches a chunk of followers with cursor.
    try {
      const { user_id, max_id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/followers/chunk', { user_id, max_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/web_profile_info', async (req, res) => {
    // Parameters: username (string, required) - The username of the user.
    // Description: Fetches web profile info for the given username.
    try {
      const { username } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/web_profile_info', { username });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/guides', async (req, res) => {
    // Parameters: user_id (string, required) - The ID of the user.
    // Description: Fetches guides for the given user ID.
    try {
      const { user_id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/guides', { user_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/by/id', async (req, res) => {
    // Parameters: id (string, required) - The ID of the media.
    // Description: Fetches the media object for the given media ID.
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/by/id', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/medias', async (req, res) => {
    try {
      const { user_id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/medias', { user_id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/medias/chunk', async (req, res) => {
    try {
      const { user_id, end_cursor } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/medias/chunk', { user_id, end_cursor });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/medias/pinned', async (req, res) => {
    try {
      const { user_id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/medias/pinned', { user_id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/clips', async (req, res) => {
    try {
      const { user_id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/clips', { user_id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/search/following', async (req, res) => {
    try {
      const { user_id, query } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/search/following', { user_id, query });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/following', async (req, res) => {
    try {
      const { user_id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/following', { user_id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/following/chunk', async (req, res) => {
    try {
      const { user_id, max_id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/following/chunk', { user_id, max_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/followers', async (req, res) => {
    try {
      const { user_id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/followers', { user_id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/followers/chunk', async (req, res) => {
    try {
      const { user_id, max_id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/followers/chunk', { user_id, max_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/web_profile_info', async (req, res) => {
    try {
      const { username } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/web_profile_info', { username });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/user/guides', async (req, res) => {
    try {
      const { user_id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/user/guides', { user_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/by/id', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/by/id', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/by/code', async (req, res) => {
    try {
      const { code } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/by/code', { code });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/by/url', async (req, res) => {
    try {
      const { url } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/by/url', { url });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/insight', async (req, res) => {
    try {
      const { media_id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/insight', { media_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/comments/chunk', async (req, res) => {
    try {
      const { id, min_id, max_id, can_support_threading } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/comments/chunk', { id, min_id, max_id, can_support_threading });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/comments', async (req, res) => {
    try {
      const { id, amount } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/comments', { id, amount });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/likers', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/likers', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/user', async (req, res) => {
    try {
      const { media_id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/user', { media_id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/oembed', async (req, res) => {
    try {
      const { url } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/oembed', { url });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/download/photo', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/download/photo', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/download/photo/by/url', async (req, res) => {
    try {
      const { url } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/download/photo/by/url', { url });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/download/video', async (req, res) => {
    try {
      const { id } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/download/video', { id });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/download/video/by/url', async (req, res) => {
    try {
      const { url } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/download/video/by/url', { url });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/code/from/pk', async (req, res) => {
    try {
      const { pk } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/code/from/pk', { pk });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/media/download/video/by/url', async (req, res) => {
    try {
      const { url } = req.query;
      const data = await hikerApiRequest('GET', '/v1/media/download/video/by/url', { url });
      res.json(data);
    } catch (error) {
      res.status(error.response?.status || 500).json({ error: error.message });
    }
  });
  
  router.get('/hashtag/medias/recent/chunk', async (req, res) => {
      try {
        const { name, max_id } = req.query;
        const data = await hikerApiRequest('GET', '/v1/hashtag/medias/recent/chunk', { name, max_id });
        res.json(data);
      } catch (error) {
        res.status(error.response?.status || 500).json({ error: error.message });
      }
    });
    
    router.get('/hashtag/medias/top/recent/chunk', async (req, res) => {
      try {
        const { name, max_id } = req.query;
        const data = await hikerApiRequest('GET', '/v1/hashtag/medias/top/recent/chunk', { name, max_id });
        res.json(data);
      } catch (error) {
        res.status(error.response?.status || 500).json({ error: error.message });
      }
    });
    
    router.get('/hashtag/medias/clips', async (req, res) => {
      try {
        const { name, amount } = req.query;
        const data = await hikerApiRequest('GET', '/v1/hashtag/medias/clips', { name, amount });
        res.json(data);
      } catch (error) {
        res.status(error.response?.status || 500).json({ error: error.message });
      }
    });
    
    router.get('/hashtag/medias/clips/chunk', async (req, res) => {
      try {
        const { name, max_id } = req.query;
        const data = await hikerApiRequest('GET', '/v1/hashtag/medias/clips/chunk', { name, max_id });
        res.json(data);
      } catch (error) {
        res.status(error.response?.status || 500).json({ error: error.message });
      }
    });
    
    router.get('/highlight/by/id', async (req, res) => {
      try {
        const { id } = req.query;
        const data = await hikerApiRequest('GET', '/v1/highlight/by/id', { id });
        res.json(data);
      } catch (error) {
        res.status(error.response?.status || 500).json({ error: error.message });
      }
    });
    
    router.get('/highlight/by/url', async (req, res) => {
      try {
        const { url } = req.query;
        const data = await hikerApiRequest('GET', '/v1/highlight/by/url', { url });
        res.json(data);
      } catch (error) {
        res.status(error.response?.status || 500).json({ error: error.message });
      }
    });
    
    router.get('/share/by/code', async (req, res) => {
      try {
        const { code } = req.query;
        const data = await hikerApiRequest('GET', '/v1/share/by/code', { code });
        res.json(data);
      } catch (error) {
        res.status(error.response?.status || 500).json({ error: error.message });
      }
    });
    
    router.get('/share/by/url', async (req, res) => {
      try {
        const { url } = req.query;
        const data = await hikerApiRequest('GET', '/v1/share/by/url', { url });
        res.json(data);
      } catch (error) {
        res.status(error.response?.status || 500).json({ error: error.message });
      }
    });

module.exports = router;