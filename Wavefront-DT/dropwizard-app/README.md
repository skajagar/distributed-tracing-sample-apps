# Wavefront Hackathon - Dropwizard App

This is a sample Java application using Dropwizard called beachshirts (#[beachops](https://medium.com/@matthewzeier/thoughts-from-an-operations-wrangler-how-we-use-alerts-to-monitor-wavefront-71329c5e57a8)) which makes cool shirts for the beach.

## Running the Application Locally

1. `git clone` this repo and navigate to this dir:

2. ```bash
   git clone https://github.com/wavefrontHQ/hackathon.git
   cd hackathon/Wavefront-DT/dropwizard-app
   ```

3. Run `mvn clean install` from the root directory of the project.

4. Now run all the services using the commands below:

   ```bash
   java -jar ./shopping/target/shopping-1.0-SNAPSHOT.jar server ./shopping/app.yaml
   java -jar ./styling/target/styling-1.0-SNAPSHOT.jar server ./styling/app.yaml
   java -jar ./delivery/target/delivery-1.0-SNAPSHOT.jar server ./delivery/app.yaml
   ```

- Use `./loadgen.sh {interval}` in the root directory to send a request of ordering shirts every `{interval}` seconds. You will see some random failures which are added by us.
- This app is instrumented with a NoopTracer. Next step is to switch from NoopTracer to WavefrontTracer to see the traces emitted from beachshirts application to Wavefront.

## Use Wavefront Tracer

1. Add dependency of [`Wavefront Opentracing SDK`](https://github.com/wavefrontHQ/wavefront-opentracing-sdk-java) to the `pom.xml`:

   ```xml
   <dependencies>
     ...
     <dependency>
       <groupId>com.wavefront</groupId>
       <artifactId>wavefront-opentracing-sdk-java</artifactId>
       <version>${latest}</version>
     </dependency>
     ...
   </dependencies>
   ```

2. If you are sending tracing spans to Wavefront via Proxy, then make sure you are using proxy version >= v4.36:

   * See [here](https://docs.wavefront.com/proxies_installing.html#proxy-installation) for details on installing the Wavefront proxy.

   * Enable `traceListenerPorts` on the Wavefront proxy configuration: See [here](https://docs.wavefront.com/proxies_configuring.html#proxy-configuration-properties) for details.

      **Note**: You need to use the same tracing port (for example: `30000`) when you instantiate the `WavefrontProxyClient` (see below).

   * You can use following command to run Wavefront proxy in docker:

     ```bash
      docker run -d \
          -e WAVEFRONT_URL=https://{CLUSTER}.wavefront.com/api/ \
          -e WAVEFRONT_TOKEN={TOKEN} \
          -e JAVA_HEAP_USAGE=512m \
          -e WAVEFRONT_PROXY_ARGS="--traceListenerPorts 30000 --histogramDistListenerPorts 40000" \
          -p 2878:2878 \
          -p 4242:4242 \
          -p 30000:30000 \
          -p 40000:40000 \
          wavefronthq/proxy:latest
     ```

3. If you are sending data to Wavefront via Direct Ingestion, then make sure you have the cluster name and corresponding token from [https://{cluster}.wavefront.com/settings/profile](https://{cluster}.wavefront.com/settings/profile).

4. Go to `dropwizard-app/common/../Tracing.java` and change the `Tracer init(String service)` method to return a [WavefrontTracer](https://github.com/wavefrontHQ/wavefront-opentracing-sdk-java#set-up-a-tracer) as follows:

   ```java
   public static Tracer init(String service) throws IOException {
       WavefrontProxyClient.Builder wfProxyClientBuilder = new WavefrontProxyClient.
           Builder("localhost").metricsPort(2878).tracingPort(30000).distributionPort(40000);
       WavefrontSender wavefrontSender = wfProxyClientBuilder.build();
       /**
        * TODO: You need to assign your microservices application a name.
        * For this hackathon, please prepend your name (example: "john") to the beachshirts application,
        * for example: applicationName = "john-beachshirts"
        */
       ApplicationTags applicationTags = new ApplicationTags.Builder(applicationName,
           service).build();
       Reporter wfSpanReporter = new WavefrontSpanReporter.Builder().
           withSource("wavefront-tracing-example").build(wavefrontSender);
       WavefrontTracer.Builder wfTracerBuilder = new WavefrontTracer.
           Builder(wfSpanReporter, applicationTags);
       return wfTracerBuilder.build();
   }
   ```

   After making all the code changes, run `mvn clean install` from the root directory of the project.

5. Now restart all the services again using below commands from root directory of the project.

   ```bash
   java -jar ./shopping/target/shopping-1.0-SNAPSHOT.jar server ./shopping/app.yaml
   java -jar ./styling/target/styling-1.0-SNAPSHOT.jar server ./styling/app.yaml
   java -jar ./delivery/target/delivery-1.0-SNAPSHOT.jar server ./delivery/app.yaml
   ```
6. Generate some load via loadgen - Use `./loadgen.sh {interval}` in the root directory to send a request of ordering shirts every `{interval}` seconds.

7. Go to **Applications -> Traces** in the Wavefront UI to visualize your traces. You can also go to **Applications -> Inventory** to visualize the RED metrics that are automatically derived from your tracing spans.