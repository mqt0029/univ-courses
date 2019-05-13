import java.io.*;
import java.io.BufferedReader;
import java.io.InputStreamReader;

// compile: javac *.java

// interactive play - java maxconnect4 interactive [ input_file ] [ computer-next / human-next ] [ search depth]
// one-move play    - java maxconnect4 one-move [ input_file ] [ output_file ] [ search depth]

// [ input_file ] -- the path and filename of the input file for the game
// [ computer-next / human-next ] -- the entity to make the next move. either computer or human. Can be abbreviated to either C or H. This is only used in interactive mode
// [ output_file ] -- the path and filename of the output file for the game.  this is only used in one-move mode
// [ search depth ] -- the depth of the minimax search algorithm

public class maxconnect4
{
  public static void main(String[] args)
  {
    // check for the correct number of arguments
    if( args.length != 4 ) 
    {
      System.out.println("Four command-line arguments are needed:\n"
       + "Usage: java [program name] interactive [input_file] [computer-next / human-next] [depth]\n"
       + "  or:  java [program name] one-move [input_file] [output_file] [depth]\n"
       + "  or:  java [program name] debug [ignored] [ignored] [depth]\n");

      exit_function( 0 );
    }

    // parse the input arguments
    String game_mode = args[0].toString();				    // the game mode
    String input = args[1].toString();					      // the input game file
    int depthLevel = Integer.parseInt( args[3] );  		// the depth level of the ai search

    // create and initialize the game board
    GameBoard currentGame = new GameBoard( input );
    
    // create the Ai Player
    AiPlayer aiplayer = new AiPlayer( depthLevel );
    AiPlayer debugplayer = new AiPlayer( depthLevel );

    //  variables to keep up with the game
    int playColumn = 99;				  //  the players choice of column to play

    //added helper parameters =============================================

    int h_player, c_player;
    if ( args[3].equalsIgnoreCase("computer-next") )
    {
      c_player = currentGame.getCurrentTurn();
      if (c_player == 2) h_player = 1;
      else h_player = 2;
    }
    else
    {
      h_player = currentGame.getCurrentTurn();
      if (h_player == 2) c_player = 1;
      else c_player = 2;
    }

    //end helper parameters ===============================================

    if( game_mode.equalsIgnoreCase( "interactive" ) ) 
    {
      while ( currentGame.getPieceCount() != 42 )
      {
        int current_player = currentGame.getCurrentTurn();

        // display the current game board
        System.out.println("move " + currentGame.getPieceCount() 
        + ": Player " + current_player
        + ", column " + playColumn);
        System.out.print("game state before move:\n");
        currentGame.printGameBoard();

        // print the current scores
        System.out.println( "Score: Player 1 = " + currentGame.getScore( 1 ) +
        ", Player2 = " + currentGame.getScore( 2 ) + "\n " );

        if ( currentGame.getPieceCount() == 42 ) return;

        if (current_player == c_player)
        {
          //play move
          playColumn = aiplayer.AlphaBetaDecision(currentGame);
          currentGame.playPiece(playColumn);

          // display the current game board
          System.out.println("move " + currentGame.getPieceCount() 
          + ": Player " + current_player
          + ", column " + playColumn);
          System.out.print("game state after move:\n");
          currentGame.printGameBoard();

          // print the current scores
          System.out.println( "Score: Player 1 = " + currentGame.getScore( 1 ) +
          ", Player2 = " + currentGame.getScore( 2 ) + "\n " );

          //save gameboard
          currentGame.printGameBoardToFile("computer.txt");
        }
        else
        {
          playColumn = -1;
          while (playColumn < 0 || playColumn >= 7)
          {
            BufferedReader buff = new BufferedReader( new InputStreamReader( System.in ) );
            System.out.print("Enter the column you want to play (1-7): ");
            try
            {
              playColumn = Integer.parseInt( buff.readLine() ) - 1;
            }
            catch (IOException e)
            {
              System.out.println("Problem in reading or converting. Value not set.");
              playColumn = -1;
            }

            if (playColumn < 0 || playColumn >= 7 || !currentGame.isValidPlay(playColumn)) 
            {
              System.out.println("\n############\nINVALID CHOICE!\n############\n");
              playColumn = -1;
            }
          }

          currentGame.playPiece(playColumn);

          // display the current game board
          System.out.println("move " + currentGame.getPieceCount() 
          + ": Player " + current_player
          + ", column " + playColumn);
          System.out.print("game state after move:\n");
          currentGame.printGameBoard();

          // print the current scores
          System.out.println( "Score: Player 1 = " + currentGame.getScore( 1 ) +
          ", Player2 = " + currentGame.getScore( 2 ) + "\n " );

          //save gameboard
          currentGame.printGameBoardToFile("human.txt");

        }
      }

      System.out.println("GAME ENDED!");
    } 
    else if( game_mode.equalsIgnoreCase( "one-move" ) ) 
    {
      String output = args[2].toString();       // the output game file

      if( currentGame.getPieceCount() < 42 ) 
      {
        int current_player = currentGame.getCurrentTurn();
       
        // AI play - random play
        playColumn = aiplayer.AlphaBetaDecision( currentGame );
        
        // play the piece
        currentGame.playPiece( playColumn );
      
        // display the current game board
        System.out.println("move " + currentGame.getPieceCount() 
         + ": Player " + current_player
         + ", column " + playColumn);
        System.out.print("game state after move:\n");
        currentGame.printGameBoard();
      
          // print the current scores
        System.out.println( "Score: Player 1 = " + currentGame.getScore( 1 ) +
          ", Player2 = " + currentGame.getScore( 2 ) + "\n " );
      
        currentGame.printGameBoardToFile( output );
      } 
      else 
      {
        System.out.println("\nI can't play.\nThe Board is Full\n\nGame Over");
        return;
      }
    }
    else if (game_mode.equalsIgnoreCase("debug"))
    {
      int win = 0, tie = 0, lost = 0, limit = 100;
      for (int i = 0; i < limit; i++)
      {
        //System.out.println("GAME RESET!");
        currentGame = new GameBoard(new int[6][7]);
        while (currentGame.getPieceCount() < 42)
        {
          int current_player = currentGame.getCurrentTurn();
          if (current_player == 1) 
          {
            playColumn = aiplayer.AlphaBetaDecision( currentGame );
            //System.out.println("AlphaBeta play column " + playColumn);
          }
          else 
          {
            playColumn = debugplayer.AlphaBetaDecision(currentGame);
            //playColumn = debugplayer.findBestPlayRandom(currentGame);
            //System.out.println("Random play column " + playColumn);
          }
          
          currentGame.playPiece(playColumn);
        }
        if (currentGame.getScore(1) > currentGame.getScore(2)) win++;
        else if (currentGame.getScore(1) == currentGame.getScore(2)) tie++;
        else lost++;
      }

      System.out.println("Win: " + win + "/" + limit + " | Tie: " + tie + "/" + limit + " | Lost: " + lost + "/" + limit);
    }
    else
    {
      System.out.println( "\n" + game_mode + " is an unrecognized game mode \n try again. \n" );
    }
    
    return;

  } // end of main()

  private static void exit_function( int value )
  {
    System.out.println("exiting from MaxConnectFour.java!\n\n");
    System.exit( value );
  }

} // end of class connectFour
