# Part 5 — Written Question

## Migrating from ingress-nginx to Kubernetes Gateway API with no downtime

I would migrate the 40 Ingress resources in stages rather than replacing the existing controller all at once. The goal is to preserve existing traffic while validating each migrated route.

1. **Inventory existing routes:** Document hosts, paths, TLS settings, annotations, rewrites, timeouts, authentication, and client-IP requirements. Identify controller-specific behavior that may not map directly to Gateway API.

2. **Prepare the new platform:** Select a Gateway API implementation and confirm it supports the required features. Install the Gateway API CRDs and controller, configure the Gateway listeners, certificates, and policies, and keep ingress-nginx running.

3. **Migrate and validate:** Convert a low-risk Ingress to an HTTPRoute. Verify route attachment, hostname and path matching, TLS, redirects, headers, health checks, and backend behavior. Compare responses with the existing route.

4. **Shift traffic gradually:** Move routes in batches using the available load balancer or traffic-routing mechanism. Monitor latency, error rates, and application health after each change.

5. **Maintain rollback:** Keep the existing Ingress resources and controller until the replacement is validated. If errors occur, direct traffic back to the old routes, investigate, and retry only after validation.

The main risks are incompatible annotations, differences in path matching, TLS configuration errors, and changed timeout or header behavior. I would remove ingress-nginx only after all 40 routes are migrated, application owners validate them, and monitoring confirms stable operation.