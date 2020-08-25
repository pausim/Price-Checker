import java.io.{FileNotFoundException, InputStream}
import org.apache.log4j.Logger
import org.apache.spark.sql.DataFrame
import org.apache.spark.sql.types.{DateType, DoubleType}
import org.apache.spark.sql.functions.{col, max}
import java.util.Properties

object load_prices_to_postgres extends SparkSessionObject {
  import spark.implicits._

  val propFileName: String = "config.properties"
  var user: String = ""
  var password: String = ""
  var url: String = ""
  val inputStream: InputStream = getClass.getClassLoader.getResourceAsStream(propFileName)
  var sourceFilePath: String = ""
  var sourceFileName: String = ""

  val logger: Logger = Logger.getLogger(getClass.getName)

  def main(args: Array[String]): Unit = {
    logger.info("Loading of scraped data is starting...")
    try {
      args.length == 2
      logger.info("Two arguments have been passed to application as expected")
    } catch {
      case e: Exception =>
        logger.error(" Please make sure that two arguments have " +
          "been passed to the application: file path and file name. " + e)
    }
    sourceFilePath = args(0)
    sourceFileName = args(1)
    logger.info("Following arguments have been passed: \n" +
      "Source file path: " + sourceFilePath + "\n"
      + "Source file name: " + sourceFileName)

    logger.info("Getting config properties for Postgres DB...")
    getPropValues()
    logger.info("Fetching data from source file...")
    val df_source = fetchJson(sourceFilePath + sourceFileName)
    logger.info("Fetching data from Postgres...")
    val df_target = fetchPostgres()
    logger.info("Checking if source data is newer than the one stored in Postgres...")
    if (checkDate(df_source, df_target)) {
      logger.info("Starting to write data to Postgres")
      df_source.write.format("jdbc").option("url", url)
        .option("dbtable", "learning.item_prices").option("user", user).option("password", password)
        .mode("append").save()
      logger.info("Data has been successfully loaded")
    } else {
      logger.info("No new data")
    }

  }

  def fetchJson(file_path:String): DataFrame = {
    var df = spark.read.format("json").load(file_path)

    df = df.withColumnRenamed("last_updated", "load_date")
      .withColumn("price", col("price").cast(DoubleType))
      .withColumn("load_date", col("load_date").cast(DateType))

    df.select("name", "price", "url", "load_date")
  }

  def fetchPostgres(): DataFrame = {
    val df = spark.read.format("jdbc").option("url", url)
      .option("dbtable", "learning.item_prices").option("user", user)
      .option("password", password).load()

    df
  }

  def checkDate(df1:DataFrame, df2:DataFrame): Boolean = {
    val date:String = df1.select("load_date").as[String].collect()(0)
    val date2:String = df2.select(max("load_date")).as[String].collect()(0)
    val check:Boolean = date > date2
    check
  }

  def getPropValues(): Unit = {
    try {
      val prop = new Properties

      if (inputStream != null) {
        prop.load(inputStream)
      } else {
        throw new FileNotFoundException("property file '" + propFileName + "' not found in the classpath")
      }

      user = prop.getProperty("user")
      password = prop.getProperty("password")
      url = prop.getProperty("url")

    } catch {
      case ex: Exception =>
        logger.error("Postgres config properties could not be retrieved! " + ex)
        sys.exit(1)
    } finally {
      inputStream.close()
    }
  }

}
