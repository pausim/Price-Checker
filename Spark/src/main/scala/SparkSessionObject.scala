import org.apache.spark.sql.SparkSession

class SparkSessionObject {
  val spark = SparkSession
    .builder()
    .master("local")
    .appName("ItemPrices")
    .getOrCreate()
}