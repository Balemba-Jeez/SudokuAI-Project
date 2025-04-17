import React, { useState } from 'react';
import './App.css';

function App() {
  const emptyGrid = Array(9)
  .fill(null)
  .map(() => Array(9).fill(null)); // 9x9 grid filled with nulls


  const [grid, setGrid] = useState(emptyGrid);
  const [solvedGrid, setSolvedGrid] = useState(null);
  const [visualizationSteps, setVisualizationSteps] = useState([]);

  const generatePuzzle = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/generate');
      const data = await response.json();
      setGrid(data.puzzle);
    } catch (error) {
      console.error('Error generating puzzle:', error);
    }
  };

  const solveWithAI = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/solve', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ puzzle: grid }),
      });

      if (response.ok) {
        const data = await response.json();
        setSolvedGrid(data.solution);
      } else {
        console.error('Failed to solve the puzzle');
      }
    } catch (error) {
      console.error('Error solving puzzle:', error);
    }
  };

  const visualizeSolving = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/visualize', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ puzzle: grid }),
      });

      if (response.ok) {
        const data = await response.json();
        setVisualizationSteps(data.visualization);
      } else {
        console.error('Failed to visualize solving process');
      }
    } catch (error) {
      console.error('Error visualizing solving:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1 className="sudoku-title">Sudoku.com</h1>
      </header>

      <div className="game-levels">
        <span>Difficulty:</span>
        <a href="#" className="active">Easy</a>
        <a href="#">Medium</a>
        <a href="#">Hard</a>
        <a href="#">Expert</a>
        <a href="#">Master</a>
        <a href="#">Extreme</a>
      </div>

      <div className="game-container">
        <div className="game-canvas">
          {grid.map((row, rowIndex) =>
            row.map((cell, colIndex) => (
            <div key={`${rowIndex}-${colIndex}`} className="game-cell">
          {cell === 0 || cell === null ? "" : cell}
        </div>
         ))
        )}

        </div>

        <div className="right-sidebar">
          <button className="btn new-game" onClick={generatePuzzle}>Generate Puzzle</button>
          <button className="btn new-game" onClick={solveWithAI}>Solve with AI</button>
          <button className="btn new-game" onClick={visualizeSolving}>Visualize Solving</button>
        </div>
      </div>

      {/* Show solved puzzle */}
      {solvedGrid && (
        <div className="solved-puzzle">
          <h2>Solved Puzzle:</h2>
          {solvedGrid.map((row, rowIndex) => (
            <div key={rowIndex}>
              {row.map((cell, colIndex) => (
                <span key={colIndex}>{cell} </span>
              ))}
            </div>
          ))}
        </div>
      )}

      {/* Show visualization steps */}
      {visualizationSteps.length > 0 && (
        <div className="visualization-steps">
          <h2>Solving Steps:</h2>
          {visualizationSteps.map((step, index) => (
            <div key={index}>
              <h3>Step {index + 1}</h3>
              {step.map((row, rowIndex) => (
                <div key={rowIndex}>
                  {row.map((cell, colIndex) => (
                    <span key={colIndex}>{cell} </span>
                  ))}
                </div>
              ))}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
