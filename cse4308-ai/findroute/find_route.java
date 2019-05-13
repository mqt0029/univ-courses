// Tram, Minh
// mqt0029
// 1001540029
// 2019-05-13

import java.io.*;
import java.util.*;
import java.lang.Comparable;

public class find_route
{
  public static void main(String[] args) throws FileNotFoundException, IOException
  {
    ArrayList<City> map = buildmap(args);
    if (args.length == 3)
    {
      uninformed_search(map,args);
    }
    else if (args.length == 4)
    {
      informed_search(map, args);
    }
  }

  static class City implements Comparable<City>
  {
    String name;
    City parent, nextcity;
    int ccost, depth, heuristic, hcost;
    ArrayList<Road> subcities;

    public City(String s)
    {
      name = s;
      parent = nextcity = null;
      ccost = depth = hcost = 0;
      heuristic = -1;
      subcities = new ArrayList<Road>();
    }

    void addroad(Road r)
    {
      if (!subcities.contains(r)) subcities.add(r);
    }

    City source()
    {
      if (parent == null) return this;
      else
      {
        City pops = parent;
        while (pops != null)
        {
          if (pops.parent == null) return pops;
          pops = pops.parent;
        }
      }

      return null;
    }

    ArrayList<City> spawn_children(ArrayList<City> map)
    {
      ArrayList<City> children = new ArrayList<City>(0);

      for (Road r : subcities)
      {
        City newcity = new City(r.dest);
        newcity.parent = this;
        for (City c : map) if (c.name.equals(newcity.name)) 
        {
          newcity.subcities = c.subcities; 
          newcity.heuristic = c.heuristic;
          break;
        }
        newcity.ccost = r.cost + newcity.parent.ccost;
        newcity.hcost = newcity.ccost + newcity.heuristic;
        newcity.depth = newcity.parent.depth + 1;
        children.add(newcity);
      }

      return children;
    }

    public int compareTo(City c)
    {
      if (ccost == c.ccost) return name.compareTo(c.name);
      return ccost - c.ccost;
    }

    @Override
    public boolean equals(Object o)
    {
      if (o == null) return false;
      if (o == this) return true;

      City c = (City)o;
      return c.name.equals(name) && c.source().name.equals(this.source().name);
    }

    public static class Comparators 
    {
      public static Comparator<City> HEURISTIC_COMPARATOR = new Comparator<City>()
      {
        @Override
        public int compare(City a, City b)
        {
          if (a.hcost == b.hcost) return a.name.compareTo(b.name);
          else return a.hcost - b.hcost;
        }
      };
    }
  }

  static class Road implements Comparable<Road>
  {
    String dest;
    int cost;

    public Road(String d, String c)
    {
      dest = d;
      cost = Integer.valueOf(c);
    }

    public int compareTo(Road r)
    {
      if (cost == r.cost) return dest.compareTo(r.dest);
      return cost - r.cost;
    }

    @Override
    public boolean equals(Object o)
    {
      if (o == null) return false;
      if (o == this) return true;

      Road r = (Road)o;

      return r.cost == cost && dest.equals(r.dest);
    }
  }

  static ArrayList<City> buildmap(String[] params) throws FileNotFoundException, IOException
  {
    ArrayList<City> map = new ArrayList<City>();
    BufferedReader breader = new BufferedReader(new FileReader(new File(params[0])));
    String line;
    while (!(line = breader.readLine()).equals("END OF INPUT"))
    {
      String[] info = line.split(" ");
      City a = new City(info[0]);
      City b = new City(info[1]);
      if (map.contains(a) && map.contains(b))
      {
        map.get(map.indexOf(a)).addroad(new Road(info[1],info[2]));
        map.get(map.indexOf(b)).addroad(new Road(info[0],info[2]));
      }
      else if (!map.contains(a) && map.contains(b))
      {
        map.add(a);
        map.get(map.indexOf(a)).addroad(new Road(info[1],info[2]));
        map.get(map.indexOf(b)).addroad(new Road(info[0],info[2]));
      }
      else if (map.contains(a) && !map.contains(b))
      {
        map.add(b);
        map.get(map.indexOf(a)).addroad(new Road(info[1],info[2]));
        map.get(map.indexOf(b)).addroad(new Road(info[0],info[2]));
      }
      else
      {
        map.add(a);
        map.add(b);
        map.get(map.indexOf(a)).addroad(new Road(info[1],info[2]));
        map.get(map.indexOf(b)).addroad(new Road(info[0],info[2]));
      }
    }

    if (params.length == 4) //heuristics available
    {
      File heur_data = new File(params[3]);
      if (heur_data.exists() && !heur_data.isDirectory())
      {
        String heurreader;
        BufferedReader hbuffer = new BufferedReader(new FileReader(heur_data));
        while (!(heurreader = hbuffer.readLine()).equals("END OF INPUT"))
        {
          String[] hinfo = heurreader.split(" ");
          for (City c : map) if (c.name.equals(hinfo[0])) c.heuristic = Integer.valueOf(hinfo[1]);
        }
      }
    }

    Collections.sort(map);
    for (City c : map) Collections.sort(c.subcities);

    return map;
  }

  static void uninformed_search(ArrayList<City> map, String[] args)
  {
    int exp_count = 0;
    ArrayList<City> expanded = new ArrayList<City>();
    ArrayList<City> fringe = new ArrayList<City>();
    String begin = args[1], end = args[2];

    for (City c : map) if (c.name.equals(begin)) {fringe.add(c); break;}

    while(!fringe.isEmpty())
    {
      /*
      //DEBUG MESSAGES
      System.out.println("Node expanded: " + exp_count);
      System.out.print("Fringe:\n");
      for (City c : fringe) System.out.println("   " + c.name + ": g(n)=" + c.ccost + ", d=" + c.depth);
      System.out.print("Closed:\n   [");
      for (City c : expanded) System.out.print("'" + c.name + "',");
      System.out.print("]\n");
      */

      City current = fringe.remove(0);
      exp_count++;

      if (!expanded.contains(current))
      {
        expanded.add(current);
        if (current.name.equals(end)) break;
        for (City c : current.spawn_children(map)) fringe.add(c);
        Collections.sort(fringe);
      }
    }

    printresult(expanded, begin, end, exp_count);
  }  

  static void informed_search(ArrayList<City> map, String[] args) throws FileNotFoundException, IOException
  {
    int exp_count = 0;
    ArrayList<City> expanded = new ArrayList<City>();
    ArrayList<City> fringe = new ArrayList<City>();
    String begin = args[1], end = args[2];

    for (City c : map) if (c.name.equals(begin)) {fringe.add(c); break;}

    while (!fringe.isEmpty())
    {
      /*
      //DEBUG MESSAGEs
      System.out.println("Node expanded: " + exp_count);
      System.out.print("Fringe:\n");
      for (City c : fringe) System.out.println("   " + c.name + ": g(n)=" + c.ccost + ", f(n)=" + c.hcost + ", h(n)=" + c.heuristic);
      System.out.print("Closed:\n   [");
      for (City c : expanded) System.out.print("'" + c.name + "',");
      System.out.print("]\n");
      */

      City current = fringe.remove(0);
      exp_count++;
      if (!expanded.contains(current))
      {
        expanded.add(current);
        if (current.name.equals(end)) break;
        for (City c : current.spawn_children(map)) fringe.add(c);
        Collections.sort(fringe, City.Comparators.HEURISTIC_COMPARATOR);
      }
    }

    printresult(expanded, begin, end, exp_count);
  }

  static void printresult(ArrayList<City> explored, String begin, String end, int count)
  {
    System.out.println("nodes expanded: " + count);
    Collections.sort(explored);
    City finalcity = null;

    for (City c : explored) if (c.name.equals(end)) { finalcity = c; break; }

    if (finalcity == null)
    {
      System.out.println("distace: infinity");
      System.out.println("route:\nnone");
    }
    else if (finalcity.name.equals(begin))
    {
      System.out.println("distace: 0 km");
      System.out.println("route:\nnone-already at destination");
    } 
    else
    {
      System.out.println("distance: " + finalcity.ccost + " km");
      while (true)
      {
        if (finalcity.parent == null) break;
        finalcity.parent.nextcity = finalcity;
        finalcity = finalcity.parent;
      }
      while (finalcity.nextcity != null)
      {
        System.out.println(finalcity.name + " to " + finalcity.nextcity.name + ", " + (finalcity.nextcity.ccost - finalcity.ccost) + " km");
        finalcity = finalcity.nextcity;
      }
    }
  }  
}