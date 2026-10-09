# Findings — Part 4 debug lab

## Defect 1 — Migration Job restart policy

**Symptom:** The migration workload was defined with `restartPolicy: Always`, which is invalid for a Kubernetes Job.

**Cause:** The Job pod template used a restart policy incompatible with Job workloads.

**Fix:** Changed `restartPolicy` to `Never`, so a completed migration container can terminate as expected.

**How I found it:** Inspected the migration Job template and corrected its pod restart policy.

## Defect 2 — Reporter RoleBinding subject

**Symptom:** The reporter ServiceAccount did not have the intended permissions through the RoleBinding.

**Cause:** The RoleBinding referenced the `default` ServiceAccount instead of `reporter`.

**Fix:** Updated the RoleBinding subject to `reporter`.

**How I found it:** Inspected the RBAC template and verified permissions using `kubectl auth can-i list pods --as=system:serviceaccount:debug-lab:reporter -n debug-lab`. The result was `yes`.

## Defect 3 — Gateway backend URL

**Symptom:** The gateway's configured backend URL used `backend.default.svc`.

**Cause:** The URL targeted the `default` namespace rather than the release namespace, `debug-lab`.

**Fix:** Changed the URL to `http://backend.debug-lab.svc:8080`.

**How I found it:** Inspected the Helm values and tested the gateway `/status` endpoint. The latest verification passed the gateway backend check.

## Defect 4 — Metrics CPU resources

**Symptom:** The metrics workload requested 2 CPU cores and had a 4-core CPU limit, exceeding the protected namespace's configured maximum of 1 core per container.

**Cause:** The chart's CPU resources exceeded the namespace LimitRange.

**Fix:** Changed the metrics CPU request to `50m` and limit to `200m`.

**How I found it:** Compared the chart's resource settings with the protected namespace constraints.

## Defect 5 — Non-numeric image user and worker cache

**Symptom:** Kubernetes initially rejected containers using `runAsNonRoot: true` because the image specified the username `nonroot`, which Kubernetes could not verify as a non-root numeric UID. The worker also logged that `/var/cache/app` was read-only.

**Cause:** The pod security context did not specify a numeric UID, and the worker had no writable volume mounted at its required cache directory.

**Fix:** Added `runAsUser: 65532` to the six workload templates. Added an `emptyDir` volume mounted at `/var/cache/app` for the worker while retaining `readOnlyRootFilesystem: true`.

**How I found it:** Inspected pod events and worker logs, then examined the image's `/etc/passwd` to confirm UID 65532 belongs to `nonroot`.

## Defect 6 — Application port and unresolved reporter parsing failure

**Symptom:** The image initially listened on port 8081 while chart probes and services targeted port 8080. After configuring `PORT: "8080"`, backend, gateway, worker, and metrics passed their readiness checks. The reporter remains unready and logs `pod list failed: parse pod list: unexpected end of JSON input`; its `/healthz` endpoint returns 503.

**Cause:** The port mismatch was confirmed and corrected. The reporter's JSON parsing failure is still unresolved; its precise root cause has not been established.

**Fix:** Added `PORT: "8080"` to the environment settings for backend, gateway, worker, reporter, and metrics. No speculative fix was applied to the reporter parsing issue.

**How I found it:** Compared application logs with readiness probe ports, reran the verification script, and inspected the newer reporter pod's logs. A separate diagnostic pod using the reporter ServiceAccount received a valid Kubernetes PodList JSON response, so the cause of the application's parsing failure remains undetermined.

## Final verification status

Latest observed result: **9 checks passing, 2 checks failing**. The remaining failures are reporter Deployment readiness and the reporter `/report` pod-count check. The gateway check passed on the latest run.

The reporter issue remains unresolved; further investigation would need to establish what response the application actually receives and why its parser rejects it.
