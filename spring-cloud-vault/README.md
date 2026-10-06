# spring-cloud-vault

Spring Boot 3.3.2 app (`OrdersApp.java`) that reads `orders.db.password` from Vault KV through Spring Cloud 2023.0.2, with an integration test using Testcontainers.

## Goal

Show how Spring Cloud Vault pulls configuration from Vault at startup, so the secret is not in any file of the application.

## Run it

```
mvn -q verify
```

Expected: `VaultConfigIT` passes. It starts `hashicorp/vault:1.17.2` in a container, writes `secret/orders-app` with `orders.db.password=from-vault`, and checks that the injected property equals `from-vault`. Not run end to end here: it needs Docker for Testcontainers and Maven dependency downloads, and neither was exercised.

## What it proves

- `application.yml` has `spring.config.import: vault://` and uses the KV backend `secret`; the application name `orders-app` selects the path `secret/orders-app`.
- `OrdersApp.java` takes `@Value("${orders.db.password}")` and prints only the length, never the value.
- `VaultConfigIT.java` overrides the Vault URI and token with `@DynamicPropertySource` to point at the container.

## Trade-offs

- Authentication is a static token (`VAULT_TOKEN`); production would use Kubernetes or AppRole auth.
- Values are read once at startup; changing the secret in Vault needs a restart or a refresh mechanism.
- The test is an integration test run by Failsafe, so `mvn test` alone does not execute it.

## When not to use it

- If you already deliver secrets as environment variables or mounted files (for example with External Secrets Operator), the extra Vault dependency adds little.
- For apps that are not Spring-based.
