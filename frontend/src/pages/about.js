
import React, { useState , useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchRecipes } from '../redux/recipeAction';
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import { Container } from 'react-bootstrap';
import vars from "../vars";
import { FaHeart, FaRegHeart, FaComment } from 'react-icons/fa';


export const About = () => {
  const dispatch = useDispatch();
  const { loading, recipes, error } = useSelector(state => state);

  useEffect(() => {
    dispatch(fetchRecipes());
  }, [dispatch]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  const RecipeCard = ({recipe}) => {
    const [liked, setLiked] = useState(false);
    const handleLikeClick = () => {
      setLiked(!liked);
    };

    return (
      <Card style={{ width: '18rem', margin: '10px' }} className='bg-success'>
        <Card.Img variant="top" src={recipe.header_image || "https://via.placeholder.com/100"} />
        <Card.Body>
          <Card.Title>{recipe.name}</Card.Title>
          <Card.Text>
            {recipe.description}
          </Card.Text>
          <div>
            <button style={{ ...heartButtonStyle, ...(liked && heartButtonLikedStyle) }} onClick={handleLikeClick}>
              {liked ? <FaHeart /> : <FaRegHeart />}
            </button>
            <Button variant="primary" style={commentButtonStyle}>
              <FaComment /> Comment
            </Button>
          </div>
        </Card.Body>
      </Card>
    );
  }

  return (
    <div>
      <h1 style={itemStyle}>All Recipes</h1>
      <Container style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-between' }}>
        {recipes.recipes.map((recipe) => (
          <RecipeCard key={recipe.id} recipe={recipe} />
        ))}
      </Container>
      {/* Add responsive space below the cards */}
      <div style={{ height: '5vw' }}></div>
    </div>
  );
};

const heartButtonStyle = {
  background: 'none',
  border: 'none',
  cursor: 'pointer',
  outline: 'none',
  padding: '0',
  color: 'gray',
  fontSize: '24px',
};

const heartButtonLikedStyle = {
  color: 'red',
};

const commentButtonStyle = {
  marginLeft: '10px',
  bgColor: vars.primary,
};

const itemStyle = {
  marginBottom: '20px',
  marginTop: '20px', 
  textTransform: "uppercase",
  fontFamily: "Raleway, sans-serif",
  letterSpacing: "3px",
  fontSize: "1rem",
  color: vars.text,
  marginLeft: '100px', // Add space to the left
  '@media (max-width: 768px)': {
    marginLeft: '0', // Reset space to the left for smaller screens
  }
};




   
 