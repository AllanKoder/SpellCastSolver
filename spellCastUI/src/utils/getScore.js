export const getScore = async (matrix, subsitutions = 0, doubleLetter = [], doubleWord = [], tripleLetter = []) => {
    const result = {
        data: null,
        error: null
    };

    if (matrix == null)
    {   
        result.error = "matrix is null"
        return result
    }
    for (const row of matrix) {
        for (const cell of row) {
          if (cell === null || cell === '') {
            result.error = 'Error: All spots in the matrix must be filled.';

            return result;
          }
        }
    }

    try {
      const response = await fetch(`/api/score/${subsitutions}`, {
        method: 'POST', // Set the method to POST
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "matrix": matrix,
          "double_word": doubleWord,
          "double_letter": doubleLetter,
          "triple_letter": tripleLetter,
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();

      console.log(data)
      result.data = data
      return result    
    } 
    catch (error) {
      result.error = "fetch error" 
      return result
    }
};