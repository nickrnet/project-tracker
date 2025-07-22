#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from opentelemetry import trace
from opentelemetry.instrumentation.django import DjangoInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
from opentelemetry.instrumentation.sqlite3 import SQLite3Instrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    )
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased


# Create resource with service information
resource = Resource(attributes={
    SERVICE_NAME: "project-tracker"
    })

# Create and configure the tracer provider
sampler = TraceIdRatioBased(0.1)
provider = TracerProvider(resource=resource, sampler=sampler)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Set the global default tracer provider
trace.set_tracer_provider(provider)

# Create a tracer from the global tracer provider
tracer = trace.get_tracer("project.tracker")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tracker.settings')
    # Initialize OpenTelemetry instrumentation
    DjangoInstrumentor().instrument()
    Psycopg2Instrumentor().instrument()
    SQLite3Instrumentor().instrument()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
            ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
