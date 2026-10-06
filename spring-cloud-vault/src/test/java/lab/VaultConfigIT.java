package lab;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.vault.VaultContainer;

@SpringBootTest
class VaultConfigIT {
    static final VaultContainer<?> VAULT = new VaultContainer<>("hashicorp/vault:1.17.2")
            .withVaultToken("dev-only-token")
            .withInitCommand("kv put secret/orders-app orders.db.password=from-vault");

    static {
        VAULT.start();
    }

    @DynamicPropertySource
    static void vault(DynamicPropertyRegistry r) {
        r.add("spring.cloud.vault.uri", () -> "http://" + VAULT.getHost() + ":" + VAULT.getMappedPort(8200));
        r.add("spring.cloud.vault.token", () -> "dev-only-token");
    }

    @Value("${orders.db.password}")
    String password;

    @Test
    void secretIsInjectedFromVault() {
        assertEquals("from-vault", password);
    }
}
