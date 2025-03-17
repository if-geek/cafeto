from typing import Any, Dict

import pytest

from cafeto import App, responses
from cafeto.testclient import TestClient
from cafeto.mvc import BaseController
from cafeto.dependency_injection import ServiceCollection

from tests.data import (
    AGeneratorSingleton,
    ExampleSingleton,
    AServiceSingleton,
    GeneratorScoped,
    GeneratorSingleton,
    GeneratorTransient,
    ModelDependencyInjectionDto,
    ServiceSingleton,
    ExampleScoped,
    AServiceScoped,
    ServiceScoped,
    ExampleTransient,
    AServiceTransient,
    ServiceTransient,
    generate_model_data
)


example_singleton: ExampleSingleton = None
service_singleton: ServiceSingleton = None
example_scoped: ExampleScoped = None
service_scoped: ServiceScoped = None
example_transient: ExampleTransient = None
service_transient: ServiceTransient = None

example_scoped_from_service_scoped: ExampleScoped = None
example_scoped_from_service_transiend: ExampleScoped = None
example_scoped_from_action: ExampleScoped = None

example_transient_from_service_transient: ExampleTransient = None
example_transient_from_service_scoped: ExampleTransient = None
example_transient_from_action: ExampleTransient = None

generator_transient: GeneratorTransient = None
generator_scoped: GeneratorScoped = None
generator_singleton: GeneratorSingleton = None


@pytest.fixture(autouse=True)
def app_setup():
    app: App = App()

    @app.controller()
    class DependencyController(BaseController):

        @app.get('/get-singleton')
        async def singleton(self, p_service_singleton: AServiceSingleton) -> None:
            global service_singleton

            service_singleton = p_service_singleton
            return responses.NoContent()
        

        @app.get('/get-scoped')
        async def scoped(self, p_service_singleton: AServiceSingleton, p_service_scoped: AServiceScoped, p_example_scoped: ExampleScoped) -> None:
            global service_singleton
            global service_scoped

            global example_scoped_from_service_scoped
            global example_scoped_from_action

            service_singleton = p_service_singleton
            service_scoped = p_service_scoped
            example_scoped_from_service_scoped = p_service_scoped.example_scoped
            example_scoped_from_action = p_example_scoped
            return responses.NoContent()
        
        @app.get('/get-transient')
        async def transient(self,
                        p_service_singleton: AServiceSingleton,
                        p_service_scoped: AServiceScoped,
                        p_service_transient: AServiceTransient,
                        p_example_scoped: ExampleScoped,
                        p_exaple_transient: ExampleTransient) -> None:
            
            global service_singleton
            global service_scoped
            global service_transient

            global example_scoped_from_service_scoped
            global example_scoped_from_service_transiend
            global example_scoped_from_action

            global example_transient_from_service_transient
            global example_transient_from_service_scoped
            global example_transient_from_action

            service_singleton = p_service_singleton
            service_scoped = p_service_scoped
            service_transient = p_service_transient

            example_scoped_from_service_scoped = p_service_scoped.example_scoped
            example_scoped_from_service_transiend = p_service_transient.example_scoped
            example_scoped_from_action = p_example_scoped

            example_transient_from_service_transient = p_service_transient.example_transient
            example_transient_from_service_scoped = p_service_scoped.example_transient
            example_transient_from_action = p_exaple_transient
            
            return responses.NoContent()
        
        @app.post('/model-dependency-injection')
        async def model_dependency_injection(self, data: ModelDependencyInjectionDto) -> str:
            return responses.Ok(data.optional_field_str)


    app.map_controllers()

    app.add_singleton(AServiceSingleton, ServiceSingleton)
    app.add_singleton(ExampleSingleton)

    def genetor_singleton(**params: Dict[str, Any]) -> GeneratorSingleton:
        params['other'] = 'generator_singleton'
        return GeneratorSingleton(**params)

    app.add_singleton(
        AGeneratorSingleton,
        GeneratorSingleton,
        genetor_singleton
    )

    app.add_scoped(AServiceScoped, ServiceScoped)
    app.add_scoped(ExampleScoped)

    def genetor_scoped(**params: Dict[str, Any]) -> GeneratorScoped:
        params['other'] = 'generator_scoped'
        return GeneratorScoped(**params)

    app.add_scoped(
        GeneratorScoped,
        genetor_scoped
    )

    app.add_transient(AServiceTransient, ServiceTransient)
    app.add_transient(ExampleTransient)

    def genetor_transient(**params: Dict[str, Any]) -> GeneratorTransient:
        params['other'] = 'generator_transient'
        return GeneratorTransient(**params)

    app.add_transient(
        GeneratorTransient,
        genetor_transient
    )

    yield TestClient(app)


def test_singleton(app_setup):
    global service_singleton

    client = app_setup

    response = client.get('/dependency/get-singleton')

    assert response.status_code == 204

    assert ServiceCollection.singleton[ExampleSingleton].value == service_singleton.example_singleton
    assert ServiceCollection.singleton[AServiceSingleton].value == service_singleton
    assert ServiceCollection.singleton[AGeneratorSingleton].value.other == 'generator_singleton'
    assert ServiceCollection.singleton[AGeneratorSingleton].value.example_singleton == service_singleton.example_singleton


def test_scoped(app_setup):
    global service_singleton
    global service_scoped
    global example_scoped_from_service_scoped

    client = app_setup

    response = client.get('/dependency/get-scoped')

    assert response.status_code == 204

    assert service_singleton.example_singleton == service_scoped.example_singleton

    assert ServiceCollection.singleton[ExampleSingleton].value == service_singleton.example_singleton
    assert ServiceCollection.singleton[AServiceSingleton].value == service_singleton

    assert ServiceCollection.singleton[ExampleSingleton].value == service_scoped.example_singleton
    assert ServiceCollection.scoped[ExampleScoped].value != service_scoped.example_scoped
    assert ServiceCollection.scoped[AServiceScoped].value != service_scoped
    assert ServiceCollection.scoped[GeneratorScoped].value != service_scoped.generator_scoped

    assert ServiceCollection.singleton[AGeneratorSingleton].value.other == 'generator_singleton'
    assert ServiceCollection.singleton[AGeneratorSingleton].value.example_singleton == service_singleton.example_singleton
    assert ServiceCollection.singleton[AGeneratorSingleton].value.example_singleton == service_scoped.example_singleton

    assert service_scoped.generator_scoped.other == 'generator_scoped'
    assert service_scoped.generator_scoped.example_singleton == service_singleton.example_singleton
    assert service_scoped.generator_scoped.example_scoped == service_scoped.example_scoped

    assert example_scoped_from_service_scoped == service_scoped.example_scoped
    assert example_scoped_from_action == example_scoped_from_service_scoped

def test_transient(app_setup):
    global service_singleton
    global service_scoped
    global service_transient

    global example_scoped_from_service_scoped
    global example_scoped_from_service_transiend
    global example_scoped_from_action

    global example_transient_from_service_transient
    global example_transient_from_service_scoped
    global example_transient_from_action

    client = app_setup

    response = client.get('/dependency/get-transient')

    assert response.status_code == 204

    assert service_singleton.example_singleton == service_scoped.example_singleton
    assert service_singleton.example_singleton == service_transient.example_singleton

    assert ServiceCollection.singleton[ExampleSingleton].value == service_singleton.example_singleton
    assert ServiceCollection.singleton[AServiceSingleton].value == service_singleton

    assert ServiceCollection.singleton[ExampleSingleton].value == service_scoped.example_singleton
    assert ServiceCollection.scoped[ExampleScoped].value != service_scoped.example_scoped
    assert ServiceCollection.scoped[AServiceScoped].value != service_scoped

    assert ServiceCollection.singleton[ExampleSingleton].value == service_transient.example_singleton
    assert ServiceCollection.scoped[ExampleScoped].value != service_transient.example_scoped
    assert ServiceCollection.transient[ExampleTransient].value != service_transient.example_transient
    assert ServiceCollection.transient[AServiceTransient].value != service_transient

    assert example_scoped_from_service_scoped == service_scoped.example_scoped
    assert example_scoped_from_service_transiend == service_transient.example_scoped
    assert example_scoped_from_action == service_scoped.example_scoped
    assert example_scoped_from_action == service_transient.example_scoped

    assert example_transient_from_service_scoped == service_scoped.example_transient
    assert example_transient_from_action != service_scoped.example_transient
    assert example_transient_from_action != service_transient.example_transient
    assert service_scoped.example_transient != service_transient.example_transient

    assert service_scoped.example_scoped == service_transient.example_scoped

    assert service_transient.generator_scoped.other == 'generator_scoped'
    assert service_transient.generator_scoped.example_singleton == service_singleton.example_singleton
    assert service_transient.generator_scoped.example_scoped == service_transient.example_scoped


def test_model_dependency_injection(app_setup):
    client = app_setup

    seed: int = 1

    data = generate_model_data(seed)
    response = client.post('/dependency/model-dependency-injection', json=data)
    assert response.status_code == 200

    response = response.text
    assert response == 'generator_scoped'
    