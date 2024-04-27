from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# Service name and Signoz endpoint configuration
SERVICE_NAME = "service_a"
SIGNOZ_ENDPOINT = "https://ingest.{region}.signoz.cloud:443"
SIGNOZ_TOKEN = "<SIGNOZ_INGESTION_KEY>"

# Set up the resource with the service name
resource = Resource.create({"service.name": SERVICE_NAME})

# Set up the trace provider
trace_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(trace_provider)

# Configure the OTLP exporter
otlp_exporter = OTLPSpanExporter(
    endpoint=SIGNOZ_ENDPOINT,
    headers={"signoz-access-token": SIGNOZ_TOKEN},
    insecure=False,
    compression="gzip"
)

# Add the span processor to the trace provider
span_processor = BatchSpanProcessor(otlp_exporter)
trace_provider.add_span_processor(span_processor)

# Get the tracer
tracer = trace.get_tracer(SERVICE_NAME)
