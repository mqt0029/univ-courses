// Tram, Minh
// mqt0029
// 1001540029
// 2019-05-13

import java.util.*;

public class AiPlayer 
{
  int depthLimit, currentDepth;

  ArrayList<Integer> evaluations;

  public AiPlayer(int d) 
  {
    depthLimit = d;
  }

  public boolean isDuplicate(GameBoard a, GameBoard b)
  {
    return Arrays.deepEquals(a.getGameBoard(), b.getGameBoard());
  }

  public boolean doesntMatter( ArrayList<Integer> target )
  {
    int comp = target.get(0);
    for (int i : target) if (i != comp) return false; 
    return true;
  }

  public ArrayList<Integer> validColumns( GameBoard currentGame )
  {
    ArrayList<Integer> result = new ArrayList<Integer>();
    for (int i = 0; i < 7; i++) if (currentGame.isValidPlay(i)) result.add(i);
    return result;
  }

  public List<GameBoard> spawnSuccessor(GameBoard currentGame)
  {
    List<GameBoard> children = new ArrayList<GameBoard>();

    for (int i = 0; i < 7; i++)
    {
      GameBoard clone = new GameBoard( currentGame.getGameBoard() );
      if (clone.isValidPlay(i)) clone.playPiece(i);
      children.add(clone);
    }

    return children;
  }

  public int strategicFill( GameBoard currentGame )
  {
    //check for opponents 3 in a row
    int player = currentGame.getCurrentTurn();
    int notplayer = (player == 1) ? 2 : 1;

    int[][] playBoard = currentGame.getGameBoard();
    
    //check vertical holes
    for( int i = 0; i < 3; i++ ) 
    {
      for( int j = 0; j < 7; j++ ) 
      {
        if  ( ( playBoard[ i ][ j ] == 0 ) &&
              ( playBoard[ i+1 ][ j ] == notplayer ) &&
              ( playBoard[ i+2 ][ j ] == notplayer ) &&
              ( playBoard[ i+3 ][ j ] == notplayer ) ) return j;
      }
    }

    //check horizontal holes
    for( int i = 0; i < 6; i++ ) 
    {
      for( int j = 0; j < 4; j++ ) 
      {
        if      ( ( playBoard[ i ][j] == notplayer ) &&
                  ( playBoard[ i ][ j+1 ] == notplayer ) &&
                  ( playBoard[ i ][ j+2 ] == notplayer ) &&
                  ( playBoard[ i ][ j+3 ] == 0 )) return j+3;

        else if ( ( playBoard[ i ][j] == notplayer ) &&
                  ( playBoard[ i ][ j+1 ] == notplayer ) &&
                  ( playBoard[ i ][ j+2 ] == 0 ) &&
                  ( playBoard[ i ][ j+3 ] == notplayer )) return j+2;

        else if ( ( playBoard[ i ][j] == notplayer ) &&
                  ( playBoard[ i ][ j+1 ] == 0 ) &&
                  ( playBoard[ i ][ j+2 ] == notplayer ) &&
                  ( playBoard[ i ][ j+3 ] == notplayer )) return j+1;

        else if ( ( playBoard[ i ][j] == 0 ) &&
                  ( playBoard[ i ][ j+1 ] == notplayer ) &&
                  ( playBoard[ i ][ j+2 ] == notplayer ) &&
                  ( playBoard[ i ][ j+3 ] == notplayer )) return j;
      }
    }

    //check diagonal / holes
    for( int i = 0; i < 3; i++ )
    {
      for( int j = 0; j < 4; j++ ) 
      {
        if      ( ( playBoard[ i+3 ][ j ] == notplayer ) &&
                  ( playBoard[ i+2 ][ j+1 ] == notplayer ) &&
                  ( playBoard[ i+1 ][ j+2 ] == notplayer ) &&
                  ( playBoard[ i ][ j+3 ] == 0 ) ) return j+3;

        else if ( ( playBoard[ i+3 ][ j ] == notplayer ) &&
                  ( playBoard[ i+2 ][ j+1 ] == notplayer ) &&
                  ( playBoard[ i+1 ][ j+2 ] == 0 ) &&
                  ( playBoard[ i ][ j+3 ] == notplayer ) ) return j+2;

        else if ( ( playBoard[ i+3 ][ j ] == notplayer ) &&
                  ( playBoard[ i+2 ][ j+1 ] == 0 ) &&
                  ( playBoard[ i+1 ][ j+2 ] == notplayer ) &&
                  ( playBoard[ i ][ j+3 ] == notplayer ) ) return j+1;

        else if ( ( playBoard[ i+3 ][ j ] == 0 ) &&
                  ( playBoard[ i+2 ][ j+1 ] == notplayer ) &&
                  ( playBoard[ i+1 ][ j+2 ] == notplayer ) &&
                  ( playBoard[ i ][ j+3 ] == notplayer ) ) return j;
      }
    }

    //check diagonal \ holes
    for( int i = 0; i < 3; i++ )
    {
      for( int j = 0; j < 4; j++ ) 
      {
        if      ( ( ( playBoard[ i ][ j ] == notplayer ) &&
                    ( playBoard[ i+1 ][ j+1 ] == notplayer ) &&
                    ( playBoard[ i+2 ][ j+2 ] == notplayer ) &&
                    ( playBoard[ i+3 ][ j+3 ] == 0 ) ) ) return j+3;

        else if   ( ( playBoard[ i ][ j ] == notplayer ) &&
                    ( playBoard[ i+1 ][ j+1 ] == notplayer ) &&
                    ( playBoard[ i+2 ][ j+2 ] == 0 ) &&
                    ( playBoard[ i+3 ][ j+3 ] == notplayer ) ) return j+2;

        else if   ( ( playBoard[ i ][ j ] == notplayer ) &&
                    ( playBoard[ i+1 ][ j+1 ] == 0 ) &&
                    ( playBoard[ i+2 ][ j+2 ] == notplayer ) &&
                    ( playBoard[ i+3 ][ j+3 ] == notplayer ) ) return j+1;

        else if   ( ( playBoard[ i ][ j ] == 0 ) &&
                    ( playBoard[ i+1 ][ j+1 ] == notplayer ) &&
                    ( playBoard[ i+2 ][ j+2 ] == notplayer ) &&
                    ( playBoard[ i+3 ][ j+3 ] == notplayer ) )  return j;
      }
    }

    //if it reached here, there is nothing to block yet, so play static column
    if (currentGame.isValidPlay(3)) return 3;
    else if (currentGame.isValidPlay(1)) return 1;
    else if (currentGame.isValidPlay(6)) return 6;

    //if no static column available and nothing to block, play random
    else return findBestPlayRandom(currentGame);
  }

  public int MaxValue(GameBoard board, int alpha, int beta )
  {
    if (board.getPieceCount() == 42) return board.terminalEvaluation();
    else if (currentDepth == depthLimit) return board.evaluation();

    currentDepth++;

    int v = Integer.MIN_VALUE;
    int index = 0;
    
    for (GameBoard b : spawnSuccessor(board))
    {
      if (!isDuplicate(b, board))
      {
        v = Math.max(v, MinValue(board, alpha, beta));

        evaluations.set(index, v);
        
        if (v >= beta) return v;
        alpha = Math.max(alpha, v);
      }

      index++;
    }

    return v;
  }

  public int MinValue(GameBoard board, int alpha, int beta )
  {
    if (board.getPieceCount() == 42) return board.terminalEvaluation();
    else if (currentDepth == depthLimit) return board.evaluation();

    currentDepth++;

    int v = Integer.MAX_VALUE;

    for (GameBoard b : spawnSuccessor(board))
    {
      if (!isDuplicate(b, board))
      {
        v = Math.min(v, MaxValue(board, alpha, beta));
        if (v <= alpha) return v;
        beta = Math.min(beta, v);
      }
    }

    return v;
  }

  public int AlphaBetaDecision ( GameBoard currentGame )
  {
    currentDepth = 0;
    evaluations = new ArrayList<Integer>( Collections.nCopies(7, 0) );

    int v = MaxValue(currentGame, Integer.MIN_VALUE, Integer.MAX_VALUE);

    //if all the move are equally useless (there is no gain in playing any move),
    //look for blocking move that will prevent the opponent from scoring
    if (doesntMatter(evaluations)) return strategicFill(currentGame);

    //there is some move that will result in a better 
    //value (either from evaluation or terminalEvaluation)
    //play that move instead
    else
    {
      int result = -1;
      int maxeval = Integer.MIN_VALUE;
      for (int i = 0; i < 7; i++)
      {
        if (currentGame.isValidPlay(i))
        {
          if (evaluations.get(i) >= maxeval)
          {
            result = i;
            maxeval = evaluations.get(i);
          }
        }
      }
      return result;
    }
  }
  
  public int findBestPlayRandom( GameBoard currentGame ) 
  {
    // start random play code
    Random randy = new Random();
    int playChoice = 99;

    playChoice = randy.nextInt( 7 );

    while( !currentGame.isValidPlay( playChoice ) )
    playChoice = randy.nextInt( 7 );

    // end random play code

    return playChoice;
  }
}