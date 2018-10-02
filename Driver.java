import java.util.Scanner;
import java.math.BigInteger;
import java.util.List;

public class Driver
{

  public static void main(String[] args)
  {
    // Get big product from user.
    System.out.println("Enter an integer to unmultiply.");
    Scanner reader = new Scanner(System.in);
    BigInteger product = reader.nextBigInteger();
    reader.close();
    
    System.out.println("The complete list of factors is:");
    // "Factorize" number.
    List<BigInteger> factors = new Unmultiplier(product).unmultiply();
    int factorsLen = factors.size();
    
    // Print out factors.
    for (int factorIndex = 0; factorIndex < factorsLen; factorIndex++)
    {
      System.out.print(factors.get(factorIndex) + ", ");
    }
    
    System.out.println("1234567890 sqrt = " + Unmultiplier.roughSqrt(new BigInteger("1234567890")));
    System.out.println("456 sqrt = " + Unmultiplier.roughSqrt(new BigInteger("456")));
  }

}
