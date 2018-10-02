import java.util.*;
import java.math.BigInteger;


public class Unmultiplier
{
  private BigInteger product;

  public Unmultiplier(BigInteger product)
  {
    this.product = product;
  }

  public List<BigInteger> unmultiply()
  {
    List<BigInteger> factors = new ArrayList<BigInteger>();

    if (product.compareTo(BigInteger.ZERO) == 0
        || product.compareTo(BigInteger.ONE) == 0)
    {
      System.err.println("Error in Unmultiplier.unmultiply: Number given was "
                         + "too small.");
    }

    for (BigInteger possibleFactor = BigInteger.ONE, productSqrt = roughSqrt(product);
        possibleFactor.compareTo(productSqrt) < 0;
        possibleFactor = possibleFactor.add(BigInteger.ONE))
    {
      if (product.mod(possibleFactor) == BigInteger.ZERO)
      {
        factors.add(possibleFactor);
        factors.add(product.divide(possibleFactor));
      }
    }

    Collections.sort(factors);
    return factors;
  }

  // Finds the square root of product VERY IMPRECISELY by cutting off half-less-one of its bytes.
  public static BigInteger roughSqrt(BigInteger product)
  {
    byte[] productBytes = product.toByteArray();
    int productBytesLen = productBytes.length;
    boolean isProductBytesLenEven = productBytesLen % 2 == 0;
    int newLen = (isProductBytesLenEven)? productBytesLen / 2 : productBytesLen / 2 + 1;
    byte[] newBytes = new byte[newLen];
    
    System.out.println("[DEBUG] productBytesLen = " + productBytesLen + " newLen = " + newLen);
    // Use the last half of product's bytes.
    for (int index = (isProductBytesLenEven)? newLen : newLen - 1; index < productBytesLen; index++) {
      newBytes[index] = productBytes[index];
    }
    
    return new BigInteger(newBytes);
  }
}
