import {
  RECIPE_LOADING,
  GET_RECIPES,
  GET_DETAIL_RECIPE,
  GET_ERRORS,
  CREATE_RECIPE,
  LIKE_RECIPE,
  EDIT_RECIPE,
  DELETE_RECIPE,
  SAVE_RECIPE,
} from "./types";
import axiosInstance from "../../utils/axios";
import { tokenConfig } from "./auth";

export const getRecipes = () => (dispatch) => {
  dispatch({ type: RECIPE_LOADING });

  const config = {
    headers: {
      "Content-Type": "application/json",
    },
  };
  axiosInstance
    .get("/recipes/all", null, config)
    .then((res) => {
      console.log("action",res.data)
      dispatch({
        type: GET_RECIPES,
        payload: res.data.recipes,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_ERRORS,
        payload: err.response,
      });
    });
};

export const getDetailRecipe = (id) => (dispatch, getState) => {
  dispatch({ type: RECIPE_LOADING });

  axiosInstance
    .get(`/recipes/${id}/full`, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: GET_DETAIL_RECIPE,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_ERRORS,
        payload: err.response,
      });
    });
};

export const createRecipe = (formData) => (dispatch, getState) => {
  dispatch({ type: RECIPE_LOADING });

  axiosInstance
    .post("/recipes/create", formData, tokenConfig(getState))
    console.log(formData)
    .then((res) => {
      dispatch({
        type: CREATE_RECIPE,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_ERRORS,
        payload: err.response,
      });
    });
};

export const editRecipe = (id, formData) => (dispatch, getState) => {
  dispatch({ type: RECIPE_LOADING });

  axiosInstance
    .patch(`/recipes/${id}`, formData, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: EDIT_RECIPE,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_ERRORS,
        payload: err.response,
      });
    });
};

export const deleteRecipe = (id) => (dispatch, getState) => {
  dispatch({ type: RECIPE_LOADING });

  axiosInstance
    .delete(`/recipes/${id}`, tokenConfig(getState))
    .then((res) => {
      console.log(res.data)
      dispatch({
        type: DELETE_RECIPE,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_ERRORS,
        payload: err.response,
      });
    });
};

export const likeRecipe = (id) => (dispatch, getState) => {
  dispatch({ type: RECIPE_LOADING });

  axiosInstance
    .post(`/recipe/${id}/like/`, null, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: LIKE_RECIPE,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_ERRORS,
        payload: err.response,
      });
    });
};

export const saveRecipe = (user_id, id) => (dispatch, getState) => {
  dispatch({ type: RECIPE_LOADING });

  const body = JSON.stringify({ id });

  axiosInstance
    .post(`/user/profile/${user_id}/bookmarks/`, body, tokenConfig(getState))
    .then((res) => {
      dispatch({
        type: SAVE_RECIPE,
        payload: res.data,
      });
    })
    .catch((err) => {
      dispatch({
        type: GET_ERRORS,
        payload: err.response,
      });
    });
};
