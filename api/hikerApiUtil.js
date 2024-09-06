const axios = require('axios');
const dotenv = require('dotenv');

dotenv.config();

const HIKERAPI_BASE_URL = 'https://api.hikerapi.com';
const HIKERAPI_ACCESS_KEY = process.env.HIKERAPI_ACCESS_KEY;

const hikerApiRequest = async (method, path, params = {}, data = {}) => {
  try {
    const response = await axios({
      method,
      url: `${HIKERAPI_BASE_URL}${path}`,
      params: {
        ...params,
        access_key: HIKERAPI_ACCESS_KEY,
      },
      data,
    });
    return response.data;
  } catch (error) {
    console.error(`Error calling HikerAPI (${path}):`, error.message);
    throw error;
  }
};

module.exports = { hikerApiRequest };