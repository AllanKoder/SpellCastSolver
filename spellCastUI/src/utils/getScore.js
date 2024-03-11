export const getScore = async (matrix) => {
    const result = {
        data: null,
        error: null
    };

    if (matrix == null)
    {   
        result.error = "matrix is null"
        console.log(result)
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
      const response = await fetch('/api/score/0', {
        method: 'POST', // Set the method to POST
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "matrix": matrix
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
  
      result.data = data
      return result    
    } 
    catch (error) {
      console.error('Fetch error:', error);

      result.error = "fetch error" 
      return result
    }
};