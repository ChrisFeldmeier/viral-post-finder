const express = require('express');
const axios = require('axios');
const dotenv = require('dotenv');
const { hikerApiRequest } = require('./hikerApiUtil'); 

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Test Media Data https://api.instagrapi.com/v2/user/medias/?user_id=62608724674&endcursor=None&access_key=
// Test User Data https://api.hikerapi.com/a2/user?username=christoph.black

// Import routes
const v1Routes = require('./routes/v1');
const v2Routes = require('./routes/v2');

// Use routes
app.use('/v1', v1Routes);
app.use('/v2', v2Routes);

// A1 endpoints
app.get('/a1/user', async (req, res) => {
  // Parameters: username (string, required) - The username of the user to fetch.
  // Description: Fetches the user object for the given username.
  try {
    const { username } = req.query;
    const data = await hikerApiRequest('GET', '/a1/user', { username });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/a1/media', async (req, res) => {
  // Parameters: code (string, required) - The code of the media to fetch.
  // Description: Fetches the media object for the given media code.
  try {
    const { code } = req.query;
    const data = await hikerApiRequest('GET', '/a1/media', { code });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/a1/media/by/id', async (req, res) => {
  // Parameters: id (string, required) - The ID of the media to fetch.
  // Description: Fetches the media object for the given media ID.
  try {
    const { id } = req.query;
    const data = await hikerApiRequest('GET', '/a1/media/by/id', { id });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/a1/media/by/url', async (req, res) => {
  // Parameters: url (string, required) - The URL of the media to fetch.
  // Description: Fetches the media object for the given media URL.
  try {
    const { url } = req.query;
    const data = await hikerApiRequest('GET', '/a1/media/by/url', { url });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/a1/hashtag', async (req, res) => {
  // Parameters: name (string, required) - The name of the hashtag to fetch.
  // Description: Fetches the hashtag object for the given hashtag name.
  try {
    const { name } = req.query;
    const data = await hikerApiRequest('GET', '/a1/hashtag', { name });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/a1/hashtag/medias/top/chunk', async (req, res) => {
  // Parameters: name (string, required) - The name of the hashtag.
  //             end_cursor (string, optional) - The end cursor for pagination.
  // Description: Fetches a chunk of top media objects for the given hashtag.
  try {
    const { name, end_cursor } = req.query;
    const data = await hikerApiRequest('GET', '/a1/hashtag/medias/top/chunk', { name, end_cursor });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/a1/hashtag/medias/recent/chunk', async (req, res) => {
  // Parameters: name (string, required) - The name of the hashtag.
  //             end_cursor (string, optional) - The end cursor for pagination.
  // Description: Fetches a chunk of recent media objects for the given hashtag.
  try {
    const { name, end_cursor } = req.query;
    const data = await hikerApiRequest('GET', '/a1/hashtag/medias/recent/chunk', { name, end_cursor });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/a1/location', async (req, res) => {
  // Parameters: id (string, required) - The ID of the location to fetch.
  // Description: Fetches the location object for the given location ID.
  try {
    const { id } = req.query;
    const data = await hikerApiRequest('GET', '/a1/location', { id });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

// A2 endpoints
app.get('/a2/user', async (req, res) => {
  // Parameters: username (string, required) - The username of the user to fetch.
  // Description: Fetches the user object for the given username.
  try {
    const { username } = req.query;
    const data = await hikerApiRequest('GET', '/a2/user', { username });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

// GQL endpoints
app.get('/gql/comments/chunk', async (req, res) => {
  // Parameters: media_id (string, required) - The ID of the media.
  //             sort_order (string, optional) - The sort order of the comments.
  //             end_cursor (string, optional) - The end cursor for pagination.
  // Description: Fetches a chunk of comments for the given media ID.
  try {
    const { media_id, sort_order, end_cursor } = req.query;
    const data = await hikerApiRequest('GET', '/gql/comments/chunk', { media_id, sort_order, end_cursor });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/comments', async (req, res) => {
  // Parameters: media_id (string, required) - The ID of the media.
  //             sort_order (string, optional) - The sort order of the comments.
  //             amount (number, optional) - The number of comments to fetch.
  //             max_requests (number, optional) - The maximum number of requests.
  // Description: Fetches comments for the given media ID.
  try {
    const { media_id, sort_order, amount, max_requests } = req.query;
    const data = await hikerApiRequest('GET', '/gql/comments', { media_id, sort_order, amount, max_requests });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/comments/threaded/chunk', async (req, res) => {
  // Parameters: media_id (string, required) - The ID of the media.
  //             comment_id (string, required) - The ID of the comment.
  //             end_cursor (string, optional) - The end cursor for pagination.
  // Description: Fetches a chunk of threaded comments for the given media and comment ID.
  try {
    const { media_id, comment_id, end_cursor } = req.query;
    const data = await hikerApiRequest('GET', '/gql/comments/threaded/chunk', { media_id, comment_id, end_cursor });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/comments/threaded', async (req, res) => {
  // Parameters: media_id (string, required) - The ID of the media.
  //             comment_id (string, required) - The ID of the comment.
  //             amount (number, optional) - The number of comments to fetch.
  // Description: Fetches threaded comments for the given media and comment ID.
  try {
    const { media_id, comment_id, amount } = req.query;
    const data = await hikerApiRequest('GET', '/gql/comments/threaded', { media_id, comment_id, amount });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/comment/likers/chunk', async (req, res) => {
  // Parameters: comment_id (string, required) - The ID of the comment.
  //             media_id (string, required) - The ID of the media.
  //             end_cursor (string, optional) - The end cursor for pagination.
  // Description: Fetches a chunk of likers for the given comment ID.
  try {
    const { comment_id, media_id, end_cursor } = req.query;
    const data = await hikerApiRequest('GET', '/gql/comment/likers/chunk', { comment_id, media_id, end_cursor });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/comment/likers', async (req, res) => {
  // Parameters: media_id (string, required) - The ID of the media.
  //             amount (number, optional) - The number of likers to fetch.
  // Description: Fetches likers for the given comment ID.
  try {
    const { media_id, amount } = req.query;
    const data = await hikerApiRequest('GET', '/gql/comment/likers', { media_id, amount });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/media/likers', async (req, res) => {
  // Parameters: media_id (string, required) - The ID of the media.
  // Description: Fetches likers for the given media ID.
  try {
    const { media_id } = req.query;
    const data = await hikerApiRequest('GET', '/gql/media/likers', { media_id });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/user/by/id', async (req, res) => {
  // Parameters: id (string, required) - The ID of the user to fetch.
  // Description: Fetches the user object for the given user ID.
  try {
    const { id } = req.query;
    const data = await hikerApiRequest('GET', '/gql/user/by/id', { id });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/user/by/username', async (req, res) => {
  // Parameters: username (string, required) - The username of the user to fetch.
  // Description: Fetches the user object for the given username.
  try {
    const { username } = req.query;
    const data = await hikerApiRequest('GET', '/gql/user/by/username', { username });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.get('/gql/user/related/profiles', async (req, res) => {
  // Parameters: id (string, required) - The ID of the user to fetch related profiles for.
  // Description: Fetches related profiles for the given user ID.
  try {
    const { id } = req.query;
    const data = await hikerApiRequest('GET', '/gql/user/related/profiles', { id });
    res.json(data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});