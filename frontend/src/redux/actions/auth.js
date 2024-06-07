import {
  REGISTER_SUCCESS,
  REGISTER_FAIL,
  LOGIN_SUCCESS,
  LOGIN_FAIL,
  LOGOUT_SUCCESS,
  GET_ERRORS,
  CLEAR_MESSAGE,
} from "./types";
import axiosInstance from "../../utils/axios";

export const register =
  ({name, username, email, password, confirmPassword }) =>
  (dispatch) => {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    if (password === confirmPassword) {
      const body = JSON.stringify({
        name,
        username,
        email,
        password,
      });

      axiosInstance
        .post("/users/register/", body, config)
        .then((res) => {
          dispatch({
            type: REGISTER_SUCCESS,
            payload: res.data,
          });
          dispatch({
            type: CLEAR_MESSAGE,
            payload: res.data,
          });
        })
        .catch((err) => {
          dispatch({
            type: GET_ERRORS,
            payload: err.response,
          });
          dispatch({
            type: REGISTER_FAIL,
          });
        });
    } else {
      dispatch({
        type: GET_ERRORS,
        payload: {
          data: { password: ["Passwords Must Match"] },
          status: null,
        },
      });
    }
  };

export const login =
  ({ username, password }) =>
  (dispatch) => {
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    const body = JSON.stringify({ username, password });

    axiosInstance
      .post("/users/login/", body, config)
      .then((res) => {
        dispatch({
          type: LOGIN_SUCCESS,
          payload: res.data,
        });
        dispatch({
          type: CLEAR_MESSAGE,
          payload: res.data,
        });
      })
      .catch((err) => {
        dispatch({
          type: GET_ERRORS,
          payload: err.response,
        });
        dispatch({
          type: LOGIN_FAIL,
        });
      });
  };

export const logout =
  ({ refresh }) =>
  (dispatch, getState) => {
    const body = JSON.stringify({ refresh });

    axiosInstance
      .post("/users/logout/", body, tokenConfig(getState))
      .then((res) => {
        dispatch({
          type: LOGOUT_SUCCESS,
        });
      })
      .catch((err) => {
        dispatch({
          type: GET_ERRORS,
          payload: err.response,
        });
      });
  };

export const tokenConfig = (getState) => {
  const token = getState().auth.token;

  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }

  return config;
};
