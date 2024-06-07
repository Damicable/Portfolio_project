import axios from "axios";

//const baseURL = "https://recipe-backend-api.herokuapp.com/api";
const baseURL = "http://127.0.0.1:5000/api";

const axiosInstance = axios.create({
  baseURL: baseURL,
  timeout: 5000,
});

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response.status === 401 &&
      originalRequest.url ===
        "/user/token/refresh/"
    ) {
      window.location.href = "/user/login/";
      return Promise.reject(error);
    }

    if (
      error.response.data.code === "token_not_valid" &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      const refreshToken = JSON.parse(localStorage.getItem("access_token")).refresh;

      return axiosInstance
        .post("/user/token/refresh/", {
          refresh: refreshToken,
        })
        .then((response) => {
          localStorage.setItem("access_token", JSON.stringify(response.data));

          axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${
            JSON.parse(localStorage.getItem("access_token")).access
          }`;

          originalRequest.headers["Authorization"] = `Bearer ${
            JSON.parse(localStorage.getItem("access_token")).access
          }`;

          return axiosInstance(originalRequest);
        });
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;

/* import axios from "axios";

// get the backend url
const baseURL = "127.0.0.1:5000/api/";

const axiosInstance = axios.create({
  baseURL: baseURL,
  timeout: 5000,
});

/* axiosInstance.interceptors.response.use(
  (response) => {
    // Check if a new access token was provided in the response
    if (response.data && response.data.access_token) {
      const newToken = response.data.access_token;
      // Update local storage with the new token
      const storedData = JSON.parse(localStorage.getItem("access_token")) || {};
      storedData.access = newToken;
      localStorage.setItem("access_token", JSON.stringify(storedData));

      // Update axios instance headers with the new token
      axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${newToken}`;
    }
    return response;
  },
  (error) => {
    if (error.response.status === 401) {
      window.location.href = "/user/login/";
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;

axiosInstance.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response.status === 401 &&
      originalRequest.url ===
        baseURL + "/user/token/refresh/"
    ) {
      window.location.href = "/user/login/";
      return Promise.reject(error);
    }

    if (
      error.response.data.code === "token_not_valid" &&
      error.response.status === 401 &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      const refreshToken = JSON.parse(localStorage.getItem("access_token")).refresh;

      return axiosInstance
        .post("/user/token/refresh/", {
          refresh: refreshToken,
        })
        .then((response) => {
          localStorage.setItem("access_token", JSON.stringify(response.data));

          axiosInstance.defaults.headers.common["Authorization"] = `Bearer ${
            JSON.parse(localStorage.getItem("access_token")).access
          }`;

          originalRequest.headers["Authorization"] = `Bearer ${
            JSON.parse(localStorage.getItem("access_token")).access
          }`;

          return axiosInstance(originalRequest);
        });
    }
    return Promise.reject(error);
  }
);

export default axiosInstance; */
